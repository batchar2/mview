import ctypes
import logging


from netpackets import transport_auth 

from factory.base_creator import BaseCreator

"""
Реализуется паттерн "Фабричный метод", для идентификации принятых пакетов.

Но сетевой пакет не требуется идентифицировать. :)
"""



class TransportAuthGetPublicKeyCreator(BaseCreator):
    """ Создатель пакета с публичным ключем, полученым от клиента """
    
    def factory_method(self, data):
        logging.info('Обработчик TransportAuthGetPublicKeyCreator')
        return transport_auth.PacketKeyAuth.from_buffer_copy(data)


class TransportAuthGetSessionKeyCreator(BaseCreator):
    """ Создатель пакета с сессионым ключем, полученым от клиента """
    
    def factory_method(self, data):
        logging.info('Обработчик TransportAuthGetSessionKeyCreator')
        return transport_auth.PacketKeyAuth.from_buffer_copy(data)


class TransportAuthUserRequestCreator(BaseCreator):
    """  Создатель пакета содержащий в себе логин и пароль """

    def factory_method(self, data):
        logging.info('Обработчик TransportAuthUserRequestCreator')
        return transport_auth.PacketUserRequestAuth.from_buffer_copy(data)