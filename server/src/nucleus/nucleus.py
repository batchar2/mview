import os
import uuid
import select
import socket
import logging

from .nuclient import NuClient


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


    def __init__(self, *, port, host, debug=None, unix_file_socket_path=None, packet_max_size=None):
        """ Конструктор класса
        :param port: номер порта, через который устанавливаются соединения
        :param host: ядрес хоста
        :param debug: режим отладки приложения
        """
        
        self._port, self._host = port, host
        self._DEBUG = debug or self._DEBUG
        self._unix_file_socket_path = unix_file_socket_path or self._unix_file_socket_path
        self._PACKET_MAX_SIZE = packet_max_size or self._PACKET_MAX_SIZE
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


    def __call__(self):

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

                    """ Обмен даннымим между клиенскими процессами """
                    self._read_unix_client_data(unix_client_socket=fd)
            

    def _create_client_process(self, *, tcp_socket):
        """Создаем новый процесс ответственный за комуникацию с ядром"""

        client_socket, addr = tcp_socket.accept()

        logging.info('Подключен клиент {0}'.format(addr))

        pid = os.fork()
        if pid == 0:
            client = NuClient(tcp_socket=client_socket, 
                                    file_chanel2nucleus=self._unix_file_socket_path,
                                    packet_max_size=self._PACKET_MAX_SIZE)

            client()
            sys.exit(0)
        
        logging.info('Создан новый процесс pid={0}'.format(pid))


    def _create_chanel_client2nucleus(self, *, unix_socket):
        """ Создается канал связи клиенский процесс-ядро системы """
        conn, addr = unix_socket.accept()
        self._clients_unix.append(conn)
        #logging.info(u'Было подключено клиенское приложение {0} {0}'.format(conn, addr))
        logging.info('Было подключено клиенское приложение')


    def _read_unix_client_data(self, *, unix_client_socket):

        #logging.info(u'Ядро <-- Клиент {0}'.format(unix_client_socket))
        logging.info('Ядро <-- Клиент')

        data = unix_client_socket.recv(self._PACKET_MAX_SIZE)

        if data:
            for fd in self._clients_unix:
                logging.info(u'Ядро --> Клиент {0}'.format(fd))
                fd.send(data)
        else:
            logging.info('Клиенский процесс отключился')
            unix_client_socket.close()
            # Костыльчик, УБРАТЬ!!!!
            sockets = []
            for fd in self._clients_unix:
                if fd != unix_client_socket:
                    sockets.append(fd)
            self._clients_unix = sockets

    def __del__(self):
        pass
