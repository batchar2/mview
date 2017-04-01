import ctypes
import logging

from abc import ABC, abstractmethod


from netpackets import chanel 

from factory.base_creator import BaseCreator

"""
Реализуется паттерн "Фабричный метод", для идентификации принятых пакетов.
"""



class PacketCreatorNormal(BaseCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('Пакет определен как CHANEL_PACKET_TYPE_NORMAL')
        return chanel.ChanelLevelPacket.from_buffer_copy(data)


class PacketCreatorClientSendPublicKey(BaseCreator):
    """  Клиент подключается и высылает свой публичный ключ """
    
    def factory_method(self, data):
        logging.info('Пакет определен как CHANEL_PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE')
        return chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)


class PacketCreatorServerSendPublicKey(BaseCreator):
    """  В ответ сервер высылает свой публичный ключ  """
    
    def factory_method(self, data):
        logging.info('Пакет определен как CHANEL_PACKET_TYPE_PUBLIC_KEY_SERVER_CLIENT_EXCHANGE')
        return chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)


class PacketCreatorClientSendPrivateSimmetricKey(BaseCreator):
    """ Клиент высылает свой закрытый симметричный ключ """

    def factory_method(self, data):
        logging.info('Получен запрос на принятие закрытого ключа CHANEL_PACKET_TYPE_PRIVATE_KEY_EXCHANGE')
        return chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)



class PacketCreatorClientAuth(BaseCreator):
    """ Клиент высылает свой логин и пароль """
    def factory_method(self, data):
        logging.info('Получен логин и пароль клиента CHANEL_PACKET_TYPE_AUTORIZATION')
        return chanel.ChanelLevelPacketUserAuth.from_buffer_copy(data)
        

class PacketCreatorQOS(BaseCreator):
    """ Создатель пакета QOS  """
    
    def factory_method(self, data):
        return chanel.ChanelLevelPacket.from_buffer_copy(data)
