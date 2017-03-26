#!/usr/bin/env python3

import os
import uuid
import select
import socket
import logging


MAX_PACKET_SIZE = 2000

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

    def __init__(self, *, port, host, debug=None, unix_file_socket_path=None):
        """ Конструктор класса
        :param port: номер порта, через который устанавливаются соединения
        :param host: ядрес хоста
        :param debug: режим отладки приложения
        """
        
        self._port, self._host = port, host
        self._DEBUG = debug or self._DEBUG
        self._unix_file_socket_path = unix_file_socket_path or self._unix_file_socket_path

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
            client = Client(tcp_socket=client_socket, file_chanel2nucleus=self._unix_file_socket_path)

            client()
            sys.exit(0)
        
        logging.info('Создан новый процесс pid={0}'.format(pid))


    def _create_chanel_client2nucleus(self, *, unix_socket):
        """ Создается канал связи клиенский процесс-ядро системы """
        conn, addr = unix_socket.accept()
        self._clients_unix.append(conn)
        logging.info(u'Было подключено клиенское приложение {0} {0}'.format(conn, addr))


    def _read_unix_client_data(self, *, unix_client_socket):

        logging.info(u'Ядро приняло на обработку данные от клиента: {0}'.format(unix_client_socket))

        data = unix_client_socket.recv(MAX_PACKET_SIZE)

        for fd in self._clients_unix:
            logging.info(u'Отправил --> {0}'.format(fd))
            fd.send(data)


    def __del__(self):
        pass




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


class Client:
    """Класс отвечающий за взаимодействие с удаленным клиентом."""

    _chanel2nucleus = None
    _tcp_socket = None
    

    def __init__(self, *, tcp_socket, file_chanel2nucleus):
        """ Конструктор класса
        :param tcp_socket: tcp-сокет, созданный при установлении связи с клиентом. 
                        Нужен для авторизации и обменом текстовых сообщений
        :param file_chanel2nucleus: имя файла-сокета, для связи с ядром
        """
        
        self._chanel2nucleus = ChanelPipeClient2Nucleus(file_chanel2nucleus)
        self._tcp_socket = tcp_socket


    def _read_nucleus2send_client(self):

        #logging.info(u'Принял данные от ядра {0}. Отправляю клиенту'.format(os.getpid()))
        data = self._chanel2nucleus.socket.recv(MAX_PACKET_SIZE)
        if data is not None:
            self._tcp_socket.send(data)

    def _read_client2send_nucleus(self):
        #logging.info(u'Принял данные от клиента {0}. Отправляю ядру'.format(os.getpid()))
        
        data = self._tcp_socket.recv(MAX_PACKET_SIZE)
        if data is not None:
            self._chanel2nucleus.socket.send(data)


    def _move_data(self, fd_read, fd_write):
        """ Перемещает данные из одного файлового дескиптора в другой
        :param fd_read: источник данных
        :param fd_write: приемник данных

        :rtype: bool
        :return: True при удачном завершении 
        """
        data = fd_read.recv(MAX_PACKET_SIZE)
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
                    self._read_client2send_nucleus()
                elif fd == self._chanel2nucleus.socket:
                    self._read_nucleus2send_client()








if __name__ == '__main__':
    nuc = Nucleus(port=9988, host='0.0.0.0', debug=True)

    nuc()