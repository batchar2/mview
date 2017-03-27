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
        """ Фабричный метод, приводит набор данных к соответствующей струтуре
        :param data: данные, полученые от пользователя 
        """
        pass


class PacketCreatorNormal(PacketCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        return ChanelLevelPacket.from_buffer_copy(data)


class PacketCreatorQOS(PacketCreator):
    """ Создатель пакета QOS  """
    
    def factory_method(self, data):
        return ChanelLevelPacket.from_buffer_copy(data)


class ChanelPacketCreator:
    """  Интерфейс, определяющий конструирование пакетов. Работа производится через него. Некий фасад  """
    
    packets_creators = {}
    
    def addAction(self, packet_type, concrete_factory, cmd):
        """ Сопоставляем тип пакета, "построитель пакета" и обработчик информации
        :param packet_type: тип, пакета
        :param concrete_factory: фабричный метод, ответственный за пакет
        :param cmd: команда, которой передается пакет для обработки
        """
        self._packets_creators[packet_type] = {
            'factory': concrete_factory,
            'cmd': cmd,
        }


    def make_packet_chanel(self, data):
        """ По данным полученым из сети строится соответствующий сетевой пакет 
        :param data: данные, полученые по сети
        """
        packet = ChanelLevelPacket.from_buffer_copy(data)

        if op.MAGIC_NUMBER == packet.field.magic:
            packet_type = packet.field.type
            # Идентифицируем пакет
            if packet_type in self._packets_creators:
                factory = self._packets_creators[paket_type]['factory']
                cmd = self._packets_creators[paket_type]['cmd']
                # Вызываем обработчик и передаем ему "распарсеный" пакет
                return cmd(factory.factory_method(data))
        return None