from abc import ABC, abstractmethod


from .packets.chanell_level import ChanelLevelPacket 

from .packets import default_options as op

"""
Реализуется паттерн "Фабричный метод", для идентификации принятых пакетов.
Продуктами являются пакеты, описанные в chanell_level.py
"""


class PacketCreator(ABC):
    """ Базовый класс создателя продукта """
    @abstractmethod
    def factory_method(self, data):
        pass


class PacketCreatorNormal(PacketCreator):
    """  Создатель "нормального пакета" """
    def __init__(self):
        pass


class PacketCreatorQOS(PacketCreator):
    """ Создатель пакета QOS  """
    def __init__(self):
        pass




class ChanelPacketCreator:
    """  Интерфейс, определяющий конструирование пакетов. Работа производится через него. Некий фасад  """
    def __init__(self):
        """ Конструктор класса. Инициализирует словарь строителей """
        self._packets_creators = {
            op.CHANEL_PACKET_TYPE_NORMAL: PacketCreatorNormal(),
            op.CHANEL_PACKET_TYPE_QOS: PacketCreatorQOS(),
        }

    def make_packet_chanel(self, data):
        """ По данным полученым из сети строится соответствующий сетевой пакет """
        packet = ChanelLevelPacket.from_buffer_copy(data)

        if op.MAGIC_NUMBER == packet.field.magic:
            packet_type = packet.field.type
            if packet_type in self._packets_creators:
                return self._packets_creators[paket_type]()
         
        return None