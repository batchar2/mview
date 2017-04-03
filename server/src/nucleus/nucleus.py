import os
import sys
import uuid
import signal
import select
import socket
import logging



#import actions
#import creators

from .nuclient.nuclient import NuClient
from .settings import SETTINGS
#from .netpackets import nucleus
from .factory.method import FactoryMethod


from .database import DataBase


class Nucleus:
    """ Ядро системы, выполняет маршрутизацию сообщений между клиентами, 
            и впреспективе, между ядрами дургих систем (горизонтальное масштабирование)
    """

    """ Слушающий серерный сокет. Используется для подключения клиентами """
    _tcp_socket = None

    """ Слушающий сокет, используется для обмена данными между клиентскими процессами """
    _unix_file_socket = None
    
    """ Список локальных клиентов-процессов (подключенных к _unix_file_socket), 
        ответственных за коммуникацию с удаленными клиентами
    """
    _clients_unix = []

    _port, _host = None, None
    """ UNIX-сокет в файловой системе """
    _unix_file_socket_path = '/tmp/nucleus.socket'
    
    """ Debug-режим """
    _DEBUG = False

    """ Максимальный размер пакета для системы """
    _PACKET_MAX_SIZE = 1300

    _SETTINGS = None

    # Фабричный метод идентификации пакетов уровня ядра
    _factory_method = None

    # сюда заносится активный клиент, с которомы в данный момент общается система
    _active_client = None 

    _data_base = None



    def __init__(self, *, port, host, settings, debug=None, unix_file_socket_path=None):
        """ Конструктор класса
        :param port: номер порта, через который устанавливаются соединения
        :param host: ядрес хоста
        :param settings: словарь настроек приложения
        :param debug: режим отладки приложения
        :param unix_file_socket_path: путь до файлового сокета, через которого осуществляется обмен с нуклиентами
        """
        
        # подтираем уничтоженные процессы       
        signal.signal(signal.SIGCHLD, self._handle_sigchld)

        self._port, self._host = port, host
        self._DEBUG = debug or self._DEBUG
        self._unix_file_socket_path = unix_file_socket_path or self._unix_file_socket_path
        self._SETTINGS = settings
        self._PACKET_MAX_SIZE = self._SETTINGS['PROTOCOLS']['PACKET_SIZE']
        """ Инициадизирую формат логгирования """
        logging_level = logging.ERROR
        if self._DEBUG:
            logging_level = logging.DEBUG
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', 
                                level=logging_level)


        logging.info('Запуск сервера {0}:{1}'.format(self._host, self._port))
        logging.info('UNIX socket-path={0}'.format(self._unix_file_socket_path))
        
        self._init_tcp_listen_socket()
        self._init_chanel2clients_socket()
        #self._init_action_nucleus_packet()

        self._data_base = DataBase()

    @property
    def data_base(self):
        return self._data_base


    def _handle_sigchld(self, signum, frame):
        """ Подтверждаем закрытие процесса """
        pid, sts = os.waitpid(-1, os.WNOHANG)


    def _init_tcp_listen_socket(self):
        """ Инициализация сетевого сокета, через который происходит инициализация соединения с клиентами """
        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._tcp_socket.bind((self._host, self._port,))        
        self._tcp_socket.listen(100)


    def _init_chanel2clients_socket(self):
        """ Инициализация канала обмена с клиентскими-процессами, ответственными за обмен данными с клиентами"""
        if os.path.exists(self._unix_file_socket_path) is True:
            os.remove(self._unix_file_socket_path)

        self._unix_file_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM )
        self._unix_file_socket.bind(self._unix_file_socket_path)
        self._unix_file_socket.listen()


    def _init_action_nucleus_packet(self):
        """ Инициализация обработчиков пакетов ядра
            Через фабричный метод.
        """
        protocol = self._SETTINGS['PROTOCOLS']['NUCLEUS']['PROTOCOL']
        self._factory_method = FactoryMethod()
        # нормальный тип пакета
        self._factory_method.addAction(packet_type=protocol['PACKET_TYPE_NORMAL'], 
                concrete_factory=creators.NucleusPacketCreatorNormal(), 
                cmd=actions.ActionTypeNormal(related_object=self))
        self._factory_method.addAction(packet_type=protocol['PACKET_TYPE_AUTORIZATION'], 
                concrete_factory=creators.NucleusPacketRequestAuth(), 
                cmd=actions.ActionTypeRequestAuth(related_object=self))


    def __call__(self):
        """ Главный цикл приложения """
        packet_size = self._SETTINGS['PROTOCOLS']['PACKET_SIZE']
        while True:
            rfds = self._clients_unix + [self._tcp_socket, self._unix_file_socket]
            fd_reads, _, e = select.select(rfds, [], [])
            for fd in fd_reads:
                if fd == self._tcp_socket:
                    """ Подключение нового клиента к системе """
                    self._create_client_process(tcp_socket=fd)
                elif fd == self._unix_file_socket:
                    """ Подключение клиентского процесса к ядру системы """
                    
                    self._create_chanel_client2nucleus(unix_socket=fd)
                else:
                   self._response_client(client=fd, packet_size=packet_size)



    def _response_client(self, *, client, packet_size):
        """ Обработка данных от клиенских процессов   """

        logging.info('Ядро <-- Клиент')
        data = client.recv(packet_size)
        if data:
            """ Получаю и парсю данные от клиенского процесса. Вызывается соответствующий обработчик """
            # предварительно сохраняю состояние, кокому клиенту следует отвечать
            self._active_client = client
            self._factory_method.response(data)

        else:
            logging.info('Клиенский процесс отключился')
            client.close()
            # Костыльчик, УБРАТЬ!!!!
            sockets = []
            for fd in self._clients_unix:
                if client != fd:
                    sockets.append(fd)
            self._clients_unix = sockets


    def send_active_nuclient_packet(self, *, packet):
        """
        Отправка данных активному клиенту
        """
        if self._active_client is not None:
            self._active_client.send(packet)
            self._active_client = None
            logging.info('Ядро --> Клиент')


    def _create_client_process(self, *, tcp_socket):
        """Создаем новый процесс ответственный за комуникацию с ядром"""

        client_socket, addr = tcp_socket.accept()

        logging.info('Подключен клиент {0}'.format(addr))

        try:
            pid = os.fork()
            if pid == 0:
                client = NuClient(tcp_socket=client_socket, file_socket_name=self._unix_file_socket_path)
                client.run()
        except BlockingIOError as e:
            logging.error('Ошибка при создании нового процесса: {0}'.format(e))
        else:
            logging.info('Создан новый процесс pid={0}'.format(pid))
        

    def _create_chanel_client2nucleus(self, *, unix_socket):
        """ Создается канал связи клиенский процесс-ядро системы """
        conn, addr = unix_socket.accept()
        self._clients_unix.append(conn)
        #logging.info(u'Было подключено клиенское приложение {0} {0}'.format(conn, addr))
        logging.info('Было подключено клиенское приложение')



    def __del__(self):
        pass

    @property
    def settings(self):
        return self._SETTINGS
