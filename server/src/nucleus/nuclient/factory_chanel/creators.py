import ctypes
import logging


from netpackets import chanel 

from factory.base_creator import BaseCreator

"""
Реализуется паттерн "Фабричный метод", для идентификации принятых пакетов.

Канальный пакет не требуется идентифицировать: по структуре все одинаковые.
"""



class ChanelPacketCreator(BaseCreator):
    """  Создатель сетевого пакета """
    
    def factory_method(self, data):
        logging.info('Обработчик ChanelPacketCreator')
        return chanel.ChanelPacket.from_buffer_copy(data)