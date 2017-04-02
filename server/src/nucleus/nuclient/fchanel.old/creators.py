import ctypes
import logging

from abc import ABC, abstractmethod


from netpackets import chanel 
from netpackets import nucleus

from factory.base_creator import BaseCreator

"""
Реализуется паттерн "Фабричный метод", для идентификации принятых пакетов.
"""



class CreatorPacketNormal(BaseCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('Обработчик CreatorPacketNormal')
        return chanel.ChanelLevelPacket.from_buffer_copy(data)


class CreatorPacketClientSendPublicKey(BaseCreator):
    """  Клиент подключается и высылает свой публичный ключ """
    
    def factory_method(self, data):
        logging.info('Обработчик CreatorPacketClientSendPublicKey')
        return chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)


class CreatorPacketServerSendPublicKey(BaseCreator):
    """  В ответ сервер высылает свой публичный ключ  """
    
    def factory_method(self, data):
        logging.info('Обработчик CreatorPacketServerSendPublicKey')
        return chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)


class CreatorPacketClientSendPrivateSimmetricKey(BaseCreator):
    """ Клиент высылает свой закрытый симметричный ключ """

    def factory_method(self, data):
        logging.info('Обработчик CreatorPacketClientSendPrivateSimmetricKey')
        return chanel.ChanelLevelPacketKeyAuth.from_buffer_copy(data)



class CreatorPacketClientAuth(BaseCreator):
    """ Клиент высылает свой логин и пароль """
    def factory_method(self, data):
        logging.info('Обработчик CreatorPacketClientAuth')
        return chanel.ChanelLevelPacketUserAuth.from_buffer_copy(data)
        

class CreatorPacketQOS(BaseCreator):
    """ Создатель пакета QOS  """
    
    def factory_method(self, data):
        logging.info('Обработчик CreatorPacketQOS')
        return chanel.ChanelLevelPacket.from_buffer_copy(data)
