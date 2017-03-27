import os
import uuid
import select
import socket
import logging

from .packets import default_options as op
from .factory_chanell_packet import PacketCreatorNormal, PacketCreatorQOS, ChanelPacketCreator
from .chanell_actions import ActionTypeNormal, ActionTypeQOS


class ChanelPipeClient2Nucleus:
    """ Канал связи от клиенского процесса до ядра системы """
    
    _sock = None

    def __init__(self, file_socket_name):
        """ Конструктор класса 
        :param file_socket_name: путь до файла-сокета, через который клиент будет вести обмен данными с ядром.
        
        """
        logging.info(u'Создается канал для ядра')

        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.connect(file_socket_name)        

    @property
    def socket(self):
        return self._sock



class ClientProcess:
    """Класс отвечающий за взаимодействие с удаленным клиентом."""

    _chanel2nucleus = None
    _tcp_socket = None
    _PACKET_MAX_SIZE = None
    
    _chanel_packet_creator = None

    def __init__(self, *, tcp_socket, file_chanel2nucleus, packet_max_size):
        """ Конструктор класса
        :param tcp_socket: tcp-сокет, созданный при установлении связи с клиентом. 
                        Нужен для авторизации и обменом текстовых сообщений
        :param file_chanel2nucleus: имя файла-сокета, для связи с ядром
        :param packet_max_size: максимальный размер пакета 
        """
        
        self._PACKET_MAX_SIZE = packet_max_size

        self._chanel2nucleus = ChanelPipeClient2Nucleus(file_chanel2nucleus)
        self._tcp_socket = tcp_socket
        self._init_action_chanell_packet()


    def _init_action_chanell_packet(self):
        """ Инициализация обработчиков пакетов канального уровня
        """
        self._chanel_packet_creator =  ChanelPacketCreator()
        self._chanel_packet_creator.addAction(packet_type=op.CHANEL_PACKET_TYPE_NORMAL, 
                concrete_factory=PacketCreatorNormal(), cmd=ActionTypeNormal(related_object=self))
        self._chanel_packet_creator.addAction(packet_type=op.CHANEL_PACKET_TYPE_QOS,
                concrete_factory=PacketCreatorQOS(), cmd=ActionTypeQOS(related_object=self))


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


    def _move_data(self, fd_read, fd_write):
        """ Перемещает данные из одного файлового дескиптора в другой
        :param fd_read: источник данных
        :param fd_write: приемник данных

        :rtype: bool
        :return: True при удачном завершении 
        """
        data = fd_read.recv(self._PACKET_MAX_SIZE)
        fd_write.send(data)
        return True


    def __call__(self):
        """ Выполняет чтение данных с каналов, декодирование и пересылка ядру системы
        """
        while True:
            # Формирую список дескрипторов, для опроса данных с них
            rfds = [self._tcp_socket, self._chanel2nucleus.socket]
            
            # Жду прихода данных на один из дескипторов
            fd_reads, _, e = select.select(rfds, [], [])
            for fd in rfds:
                if fd == self._tcp_socket:
                    data = fd.recv(self._PACKET_MAX_SIZE)
                    self._chanel_packet_creator.make_packet_chanel(data)
                    #self._read_client2send_nucleus()
                elif fd == self._chanel2nucleus.socket:
                    pass
                    #self._read_nucleus2send_client()


