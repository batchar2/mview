#!/usr/bin/env python3

import ctypes
import socket


from io import BytesIO

from nucleus.netpackets import chanel as ch
from nucleus.netpackets import options as op

from nucleus import options as base_options
class Client:

    _sock = None
    def __init__(self):
        self._sock = socket.socket()
        self._sock.connect(('localhost', 9988))
        
    def __call__(self):
        self.send_public_key()

    def send_public_key(self):
        # передача серверу открытого ключа клиента
        print('-' * 10)
        print('Передаем открытый ключ клиента')
        packet = ch.ChanelLevelPacketKeyAuth()
        packet.magic_number = base_options.MAGIC_NUMBER
        packet.type = op.CHANEL_PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE
        packet.version = op.CHANEL_PACKET_VERSION
        
        print("Data size={0}".format( ctypes.sizeof(packet)))
        self._sock.send(packet)

        # Жду ответ от сервера с его открытым ключем
        print('-' * 10)
        print('Принимаем открытый ключ сервера')
        data = self._sock.recv(op.CHANEL_PACKET_SIZE)
        packet = ch.ChanelLevelPacketKeyAuth.from_buffer_copy(data)
        print("magic_number={0}".format(packet.magic_number))
        print("length={0}".format(packet.length))
        print("key={0}".format(packet.key))

        # Передача серверу зарытый ключ
        print('-' * 10)
        print('Передаем закрытый ключ для симетричного шифрования')
        packet = ch.ChanelLevelPacketKeyAuth()
        packet.magic_number = base_options.MAGIC_NUMBER
        packet.type = op.CHANEL_PACKET_TYPE_PRIVATE_KEY_EXCHANGE
        packet.version = op.CHANEL_PACKET_VERSION
        print("Data size={0}".format( ctypes.sizeof(packet)))
        self._sock.send(packet)

        # Ждем ответа о принятии ключа
        print('-' * 10)
        print('Ждем подтверждения принятия ключа')
        data = self._sock.recv(op.CHANEL_PACKET_SIZE)
        packet = ch.ChanelLevelPacketKeyAuth.from_buffer_copy(data)
        print("ответ: {0} == {1}".format(packet.type, op.CHANEL_PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS))
        print("magic_number={0}".format(packet.magic_number))
        print("length={0}".format(packet.length))
        print("key={0}".format(packet.key))
        
        # Отправляю свои данные - логин и пароль
        packet = ch.ChanelLevelPacketUserAuth()
        packet.magic_number = base_options.MAGIC_NUMBER
        packet.type = op.CHANEL_PACKET_TYPE_AUTORIZATION
        packet.version = op.CHANEL_PACKET_VERSION
         # УБРАТЬ, сделано для тестов !!!!
        str2cubytes = lambda s, size: ctypes.cast(s, ctypes.POINTER(ctypes.c_ubyte * size))[0]
        username = str2cubytes('username', base_options.LOGIN_SIZE)
        password = str2cubytes('password', base_options.PASSWORD_SIZE)
        
        print("Data size={0}".format( ctypes.sizeof(packet)))
        self._sock.send(packet)


        print('-' * 10)
        print('Жду подтверждения авторизации')
        data = self._sock.recv(op.CHANEL_PACKET_SIZE)
        packet = ch.ChanelLevelPacketKeyAuth.from_buffer_copy(data)
        if (packet.type == op.CHANEL_PACKET_TYPE_AUTORIZATION_SUCCESS):
            print("УСПЕШНАЯ АВТОРИЗАЦИЯ")
        else:
            print("Не верный логин или пароль")

        self._sock.close()

if __name__ == '__main__':
    client = Client()
    client()