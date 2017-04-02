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
        self.send_public_key()

    def send_public_key(self):
        packet_chanel = chanel.ChanelPacket()
        packet_chanel.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_chanel.type  = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['TYPE_NOT_SECURE']
        packet_chanel.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']

        print("packet_chanelt size={0}".format( ctypes.sizeof(packet_chanel)))

        print('-' * 10)
        print('Формирую пакет для отправки открытого ключа')

        packet_network = network.NetworkMessage()
        packet_network.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_network.type = SETTINGS['PROTOCOLS']['NETWORK']['PROTOCOL']['TYPE_AUTHORIZATION']

        print("packet_network size={0}".format( ctypes.sizeof(packet_network)))

       
        
        packet_transport = transport_auth.PacketKeyAuth()
        packet_transport.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet_transport.type = SETTINGS['PROTOCOLS']['TRANSPORT']['PROTOCOL']['AUTH']['PUBLIC_KEY_СLIENT2SERVER_SEND'] 
        #packet_transport.key = 123

        print("packet_transport size={0}".format( ctypes.sizeof(packet_transport)))


        packet_network.body = (ctypes.c_ubyte * ctypes.sizeof(packet_transport)).from_buffer_copy(packet_transport)


        packet_chanel.body = (ctypes.c_ubyte * ctypes.sizeof(packet_network)).from_buffer_copy(packet_network)

        self._sock.send(packet_chanel)
        """
        # передача серверу открытого ключа клиента
        print('-' * 10)
        print('Передаем открытый ключ клиента')
        packet = chanel.ChanelLevelPacketKeyAuth()
        packet.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet.type = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE']
        packet.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']
        
        print("Data size={0}".format( ctypes.sizeof(packet)))
        self._sock.send(packet)

        # Жду ответ от сервера с его открытым ключем
        print('-' * 10)
        print('Принимаем открытый ключ сервера')
        data = self._sock.recv(SETTINGS['PROTOCOLS']['PACKET_SIZE'])
        packet = chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)
        print("magic_number={0}".format(packet.magic_number))
        print("length={0}".format(packet.length))
        #print("key={0}".format(packet.key))

        # Передача серверу зарытый ключ
        print('-' * 10)
        print('Передаем закрытый ключ для симетричного шифрования')
        packet = chanel.ChanelLevelPacketKeyAuth()
        packet.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet.type = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_TYPE_PRIVATE_KEY_EXCHANGE'] 
        
        print("Data size={0}".format( ctypes.sizeof(packet)))
        self._sock.send(packet)

        # Ждем ответа о принятии ключа
        print('-' * 10)
        print('Ждем подтверждения принятия ключа')
        data = self._sock.recv(SETTINGS['PROTOCOLS']['PACKET_SIZE'])
        packet = chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)
        print("ответ: {0} == {1}".format(packet.type, SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS']))
        print("magic_number={0}".format(packet.magic_number))
        print("length={0}".format(packet.length))
        #print("key={0}".format(packet.key))
        
        #while True:
            
        # Отправляю свои данные - логин и пароль
        packet = chanel.ChanelLevelPacketUserAuth()
        packet.magic_number = SETTINGS['PROTOCOLS']['MAGIC_NUMBER']
        packet.type =  SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_TYPE_AUTORIZATION']
        packet.version = SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_VERSION']
         # УБРАТЬ, сделано для тестов !!!!
        #str2cubytes = lambda s, size: ctypes.cast(s, ctypes.POINTER(ctypes.c_ubyte * size))[0]
        username = str2cubytes('username', SETTINGS['PROTOCOLS']['LOGIN_SIZE'])
        password = str2cubytes('password', SETTINGS['PROTOCOLS']['PASSWORD_SIZE'])
        
        packet.username = username
        packet.password = password

        u = str2cubytes('username', SETTINGS['PROTOCOLS']['LOGIN_SIZE'])
        print("user_name=", cubutes2str(u))
        print("Data size={0}".format( ctypes.sizeof(packet)))
        self._sock.send(packet)


        print('-' * 10)
        print('Жду подтверждения авторизации')
        data = self._sock.recv(SETTINGS['PROTOCOLS']['PACKET_SIZE'])
        packet = chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)
        if packet.type == SETTINGS['PROTOCOLS']['CHANEL']['PROTOCOL']['PACKET_TYPE_AUTORIZATION_SUCCESS']:
            print("УСПЕШНАЯ АВТОРИЗАЦИЯ")
        else:
            print("Не верный логин или пароль")

        self._sock.close()
        """
if __name__ == '__main__':
    #while True:
    client = Client()
    client()