import os
import sys
import uuid
import select
import socket
import logging

from factory.method import FactoryMethod

from .fchanel import actions as ch_actions
from .fchanel import creators as ch_creators

from .fnucleus import actions as nuc_actions
from .fnucleus import creators as nuc_creators


"""
Клиент ядра системы. Отвечает за связь с удаленным клиентом
"""

class ChanelPipeClient2Nucleus:
    """ Канал связи от клиенского процесса до ядра системы """
    
    _sock = None

    def __init__(self, file_socket_name):
        """ Конструктор класса 
        :param file_socket_name: путь до файла-сокета, через который клиент будет вести обмен данными с ядром.
        
        """
        logging.info('Создается канал для ядра')

        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.connect(file_socket_name)        

    @property
    def socket(self):
        return self._sock



class NuClient:
    """Класс отвечающий за взаимодействие с удаленным клиентом."""

    _chanel2nucleus = None
    _tcp_socket = None
    _SETTINGS = None
    _PACKET_MAX_SIZE = None
    
    _factory_method_user = None
    _factory_method_nucleus = None

    def __init__(self, *, tcp_socket, file_chanel2nucleus, settings):
        """ Конструктор класса
        :param tcp_socket: tcp-сокет, созданный при установлении связи с клиентом. 
                        Нужен для авторизации и обменом текстовых сообщений
        :param file_chanel2nucleus: имя файла-сокета, для связи с ядром
        :param settings: словарь настроек приложения
        """
        
        tcp_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


        self._SETTINGS = settings        
        self._PACKET_MAX_SIZE = self._SETTINGS['PROTOCOLS']['PACKET_SIZE']

        self._chanel2nucleus = ChanelPipeClient2Nucleus(file_chanel2nucleus)
        self._tcp_socket = tcp_socket

        # инициализирую обработчики данных
        self._init_action_chanell_packet()
        self._init_action_nucleus_packet()


    @property
    def settings(self):
        return self._SETTINGS


    def _init_action_chanell_packet(self):
        """ Инициализация обработчиков пакетов канального уровня
            Через фабричный метод.
        """
        self._factory_method_user = FactoryMethod()
        

        protocol = self._SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']
        # нормальный тип пакета
        self._factory_method_user.addAction(packet_type=protocol['PACKET_TYPE_NORMAL'], 
                concrete_factory=ch_creators.CreatorPacketNormal(), 
                cmd=ch_actions.ActionTypeNormal(related_object=self))
        # пакет проверки качества соединения с сервером
        self._factory_method_user.addAction(packet_type=protocol['PACKET_TYPE_QOS'],
                concrete_factory=ch_creators.CreatorPacketQOS(),
                cmd=ch_actions.ActionTypeQOS(related_object=self))
        # пакет с информацией о публичном ключе клиента
        self._factory_method_user.addAction(packet_type=protocol['PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE'],
                concrete_factory=ch_creators.CreatorPacketClientSendPublicKey(), 
                cmd=ch_actions.ActionTypeClientSendPublicKey(related_object=self))
        # пакет с закрытым-симметричный ключем клиента
        self._factory_method_user.addAction(packet_type=protocol['PACKET_TYPE_PRIVATE_KEY_EXCHANGE'],
                concrete_factory=ch_creators.CreatorPacketClientSendPrivateSimmetricKey(),
                cmd=ch_actions.ActionTypeClientSendPrivateKey(related_object=self))
        # пакет с идентификатором пользователя (логин и пароль)
        self._factory_method_user.addAction(packet_type=protocol['PACKET_TYPE_AUTORIZATION'],
                concrete_factory=ch_creators.CreatorPacketClientAuth(),
                cmd=ch_actions.ActionTypeClientAuth(related_object=self))
        

    def _init_action_nucleus_packet(self):
        """ 
        Инициализация обработчиков сообщений от ядра системы
        """
        protocol = self._SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']

        self._factory_method_nucleus = FactoryMethod()
        # пакет для пересылки пользователю
        self._factory_method_nucleus.addAction(packet_type=protocol['PACKET_TYPE_NORMAL'],
                concrete_factory=nuc_creators.CreatorPacketNormal(),
                cmd=nuc_actions.ActionNormal(related_object=self))
        # пакет о статусе неудачной авторизации
        self._factory_method_nucleus.addAction(packet_type=protocol['PACKET_TYPE_AUTORIZATION_FAIL'],
                concrete_factory=nuc_creators.CreatorPacketAuthResponseFail(),
                cmd=nuc_actions.ActionAuthResponseFail(related_object=self))
        # пакет с удачной авторизацией
        self._factory_method_nucleus.addAction(packet_type=protocol['PACKET_TYPE_AUTORIZATION_SUCCESS'],
                concrete_factory=nuc_creators.CreatorPacketAuthRespnseSuccess(),
                cmd=nuc_actions.ActionAuthResponseSucess(related_object=self))


    def _read_nucleus2send_client(self):
        #logging.info(u'Принял данные от ядра {0}. Отправляю клиенту'.format(os.getpid()))
        data = self._chanel2nucleus.socket.recv(self._PACKET_MAX_SIZE)
        if data is not None:
            self._tcp_socket.send(data)


    def _read_client2send_nucleus(self):
        #logging.info(u'Принял данные от клиента {0}. Отправляю ядру'.format(os.getpid()))
        
        data = self._tcp_socket.recv(self._PACKET_MAX_SIZE)
        if data is not None:
            self._chanel2nucleus.socket.send(data)

    
    def set_client_public_key(self, *, key):
        """ Сохраняет публичный ключ клиента 
        :param key: публичный ключ
        """
        pass


    def generate_rsa_keys(self):
        """ Генерирует ключи """


    def get_public_key(self):
        """ Получает публичный ключ """
        return "123456790"


    def send_user(self, *, packet):
        """ Отправка пользователю пакета данных """
        self._tcp_socket.send(packet)

    def decode_rsa_data(self, *, data):
        """ Расшифровать данные от клиента """
        pass


    def set_client_aes_key(self, *, key):
        """ Сохранить секретный-симетричный ключ клиента """
        pass
    

    def decode_aes(self, *, data):
        """ Расшифровать информацию полученную от пользователя """
        return data


    def request_nucleus(self, *, packet):
        """ Запрос специально сформированым пакетом к ядру системы """
        self._chanel2nucleus.socket.send(packet)
        

    def __call__(self):
        """
        Выполняет чтение данных с каналов, декодирование и пересылка ядру системы
        """

        packet_size = self._SETTINGS['PROTOCOLS']['PACKET_SIZE']

        while True:
            # Формирую список дескрипторов, для опроса данных с них
            rfds = [self._tcp_socket, self._chanel2nucleus.socket]
            

            # Жду прихода данных на один из дескипторов
            fd_reads, _, e = select.select(rfds, [], [])
            for fd in fd_reads:
                # данные от пользователя по tcp-сокету
                data = fd.recv(packet_size)
                if fd == self._tcp_socket:
                    if data:
                        self._factory_method_user.response(data)
                    else:
                        logging.info(u'Клиент отключился')
                        fd.close()
                        sys.exit(0)
                # Данные от ядра для пользователя
                elif fd == self._chanel2nucleus.socket:
                    #print('udp')
                    #print("DATA == ", data)
                    self._factory_method_nucleus.response(data)
        sys.exit(0)
                    

