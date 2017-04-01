import ctypes
import logging
from abc import ABC, abstractmethod

from netpackets import nucleus

"""
Реализуется паттерн "Фабричный метод".
Обрабатывается ядром системы
"""


class NucleusPacketCreator(ABC):
    """ Базовый класс создателя продукта """
    @abstractmethod
    def factory_method(self, data):
        """ Фабричный метод, приводит набор данных к соответствующей струтуре
        :param data: данные, полученые от пользователя 
        """
        pass


class NucleusPacketCreatorNormal(NucleusPacketCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('Пакет определен как PACKET_TYPE_NORMAL')
        pass


class NucleusPacketRequestAuth(NucleusPacketCreator):
    """  Запрос на авторизацию клиента """
    
    def factory_method(self, data):
        pass





class NucleusPacketCreator:
    """  Интерфейс, определяющий конструирование пакетов. Работа производится через него. Некий фасад  """
    
    _nucleus_creators = {}
    _SETTINGS = None
    def __init__(self, *, settings):
        self._SETTINGS = settings

    def addAction(self, *, packet_type, concrete_factory, cmd):
        """ Сопоставляем тип пакета, "построитель пакета" и обработчик информации
        :param packet_type: тип, пакета
        :param concrete_factory: фабричный метод, ответственный за пакет
        :param cmd: команда, которой передается пакет для обработки
        """
        self._nucleus_creators[packet_type] = {
            'factory': concrete_factory,
            'cmd': cmd,
        }


    def make_packet_nucleus(self, data):
        """ По данным полученым из сети строится соответствующий сетевой пакет 
        :param data: данные, полученые по сети
        """
        try:
            # выполняем преобразование данных в пакет БАЗОВОГО ФОРМАТА, для идентификации
            packet = nucleus.BaseNucleusPacket.from_buffer_copy(data)
        except Exception as e:
            logging.error(str(e))
            return None

        if packet is not None:
            logging.info('Получен пакет размера: {0} байт'.format(ctypes.sizeof(packet)))
            if self._SETTINGS['PROTOCOLS']['MAGIC_NUMBER'] == packet.magic_number:
                # Идентифицируем пакет
                if packet.type in self._nucleus_creators:
                    factory = self._nucleus_creators[packet.type]['factory']
                    cmd = self._nucleus_creators[packet.type]['cmd']
                    # Вызываем обработчик и передаем ему "распарсеный" пакет
                    return cmd(packet=factory.factory_method(data))
                else:
                    logging.error('Пакет неизвестного типа!')
            else:
                logging.error('Пакет не имеет магического числа!')
        else:
             logging.error('Пакет не распарсился')
        return None