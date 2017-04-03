#!/usr/bin/env python3

import ctypes
import socket


from io import BytesIO

#from nucleus.nuclient.fchanel.netpackets import chanel as ch
#from nucleus.nuclient.fchanel.netpackets import options as op

from nucleus.netpackets import chanel, network, transport_auth


from nucleus.settings import SETTINGS


from nucleus.cubytes import str2cubytes, cubutes2str

"""
def str2cubytes(string, size):
    return (ctypes.c_ubyte * size)(*[ctypes.c_ubyte(ord(char)) for char in string])
def cubutes2str(cubytes):
    symbols =  [chr(byte) for byte in cubytes]
    string = ""
    for symbol in symbols:
        string += symbol
    return string
"""
#from nucleus import options as base_options
class Client:

    _sock = None
    def __init__(self):
        self._sock = socket.socket()
        self._sock.connect(('localhost', 9988))
        
    def __call__(self):
        username = 'user1'
        password = 'password'
        # отправляем публичный ключ
        self.send_public_key()
        # принимаю публичный ключ сервера
        self.get_server_public_key()
        # отправляю сессионый ключ
        self.send_session_key()
        # жду подтверждения принятия сессионого ключа
        self.get_answer_session_key()
        # отправляю логин и пароль пользователя
        self.send_username_password(username, password)
        # жду ответа о статусе авторизации от сервера
        self.get_auth_packet()

    def send_public_key(self):
        print('-' * 10)
        print('Формирую пакет для отправки открытого ключа')
        packet_chanel = chanel.ChanelPacket()
        packet_chanel.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_chanel.type  = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['TYPE_NOT_SECURE']
        packet_chanel.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']

        #print("packet_chanelt size={0}".format( ctypes.sizeof(packet_chanel)))

        #print('-' * 10)
        

        packet_network = network.NetworkMessage()
        packet_network.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_network.type = SETTINGS['PROTOCOLS']['NETWORK']['PROTOCOL']['TYPE_AUTHORIZATION']

        #print("packet_network size={0}".format( ctypes.sizeof(packet_network)))

       
        
        packet_transport = transport_auth.PacketKeyAuth()
        packet_transport.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_transport.type = SETTINGS['PROTOCOLS']['TRANSPORT']['PROTOCOL']['AUTH']['PUBLIC_KEY_СLIENT2SERVER_SEND'] 
        #packet_transport.key = 123

        #print("packet_transport size={0}".format( ctypes.sizeof(packet_transport)))


        packet_network.set_body(packet_transport)
        packet_chanel.set_body(packet_network)
        #packet_network.body = (ctypes.c_ubyte * ctypes.sizeof(packet_transport)).from_buffer_copy(packet_transport)
        #packet_chanel.body = (ctypes.c_ubyte * ctypes.sizeof(packet_network)).from_buffer_copy(packet_network)

        self._sock.send(packet_chanel)

    def get_server_public_key(self):
        print('-' * 10)
        print('Формирую пакет для приема открытого ключа')
        data = self._sock.recv(SETTINGS['PROTOCOLS']['PACKET_SIZE'])
        chanel_packet = chanel.ChanelPacket.from_buffer_copy(data)
        #print("NETWORK magic_number={0}".format(chanel_packet.magic_number))

        packet_network = network.NetworkMessage.from_buffer_copy(chanel_packet.body)
        
        message = 'PUBLIC_KEY_SERVER2CLIENT_SEND'
        if packet_network.type != SETTINGS['PROTOCOLS']['TRANSPORT']['PROTOCOL']['AUTH']['PUBLIC_KEY_SERVER2CLIENT_SEND']:
            message = 'UNCOWN'

        packet_transport = transport_auth.PacketKeyAuth.from_buffer_copy(packet_network.body)
        

    def send_session_key(self):
        print('-' * 10)
        print('Формирую пакет для отправки сессионого ключа')
        packet_chanel = chanel.ChanelPacket()
        packet_chanel.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_chanel.type  = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['TYPE_NOT_SECURE']
        packet_chanel.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']

        
        #print('Формирую пакет для отправки открытого ключа')

        packet_network = network.NetworkMessage()
        packet_network.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_network.type = SETTINGS['PROTOCOLS']['NETWORK']['PROTOCOL']['TYPE_AUTHORIZATION']

        
        packet_transport = transport_auth.PacketKeyAuth()
        packet_transport.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_transport.type = SETTINGS['PROTOCOLS']['TRANSPORT']['PROTOCOL']['AUTH']['SESSION_PRIVATE_KEY'] 

        packet_network.set_body(packet_transport)
        packet_chanel.set_body(packet_network)

        self._sock.send(packet_chanel)


    def get_answer_session_key(self):
        print('-' * 10)
        print('Формирую пакет для приема ответа о успешности приема ключа сервером')
        data = self._sock.recv(SETTINGS['PROTOCOLS']['PACKET_SIZE'])
        chanel_packet = chanel.ChanelPacket.from_buffer_copy(data)
        print("NETWORK magic_number={0}".format(chanel_packet.magic_number))

        packet_network = network.NetworkMessage.from_buffer_copy(chanel_packet.body)
        
        message = 'PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS'
        if packet_network.type != SETTINGS['PROTOCOLS']['TRANSPORT']['PROTOCOL']['AUTH']['PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS']:
            message = packet_network.type


        print("Принят пакет типа = {0}".format(message))

        packet_transport = transport_auth.PacketKeyAuth.from_buffer_copy(packet_network.body)
        
        print("packet_transport magic_number={0}".format(packet_transport.magic_number))
        

    def send_username_password(self, username, password):
        print('-' * 10)
        print('Формирую пакет для отправки логина и пароля')
        packet_chanel = chanel.ChanelPacket()
        packet_chanel.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_chanel.type  = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['TYPE_NOT_SECURE']
        packet_chanel.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']

        packet_network = network.NetworkMessage()
        packet_network.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_network.type = SETTINGS['PROTOCOLS']['NETWORK']['PROTOCOL']['TYPE_AUTHORIZATION']

        packet_transport = transport_auth.PacketUserRequestAuth()
        packet_transport.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_transport.type = SETTINGS['PROTOCOLS']['TRANSPORT']['PROTOCOL']['AUTH']['PACKET_TYPE_AUTORIZATION'] 
        packet_transport.set_username(username=username)
        packet_transport.set_password(password=password)

        packet_network.set_body(packet_transport)
        packet_chanel.set_body(packet_network)


        self._sock.send(packet_chanel)


    def get_auth_packet(self):
        print('-' * 10)
        print('ловлю статус авторизации клиента')

        data = self._sock.recv(SETTINGS['PROTOCOLS']['PACKET_SIZE'])
        chanel_packet = chanel.ChanelPacket.from_buffer_copy(data)
        print("NETWORK magic_number={0}".format(chanel_packet.magic_number))

        packet_network = network.NetworkMessage.from_buffer_copy(chanel_packet.body)
        
        message = 'PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS'
        if packet_network.type != SETTINGS['PROTOCOLS']['TRANSPORT']['PROTOCOL']['AUTH']['PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS']:
            message = packet_network.type


        print("Принят пакет типа = {0}".format(message))

        packet_transport = transport_auth.PacketUserResponseAuth.from_buffer_copy(packet_network.body)
        
        print("packet_transport magic_number={0}".format(packet_transport.magic_number))

        
if __name__ == '__main__':
    #while True:
    client = Client()
    client()