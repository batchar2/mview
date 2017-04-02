import ctypes
import logging


from netpackets import network 

from factory.base_creator import BaseCreator

"""
Реализуется паттерн "Фабричный метод", для идентификации принятых пакетов.

Но сетевой пакет не требуется идентифицировать. :)
"""



class NetworkPacketCreator(BaseCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('Обработчик NetworkPacketCreator')
        return network.NetworkMessage.from_buffer_copy(data)