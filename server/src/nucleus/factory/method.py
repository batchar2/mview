# реализация фабричного метода

import ctypes
import logging
from settings import SETTINGS

from netpackets import chanel


class FactoryMethod:
    """  Интерфейс, определяющий конструирование пакетов. Работа производится через него. Некий фасад  """
    
    def __init__(self):
        self._packets_creators = {}

    def addAction(self, *, packet_type, concrete_factory, cmd):
        """ Сопоставляем тип пакета, "построитель пакета" и обработчик информации
        :param packet_type: тип, пакета
        :param concrete_factory: фабричный метод, ответственный за пакет
        :param cmd: команда, которой передается пакет для обработки
        """
        self._packets_creators[packet_type] = {
            'factory': concrete_factory,
            'cmd': cmd,
        }


    def response(self, data):
        """ По данным полученым из сети строится соответствующий сетевой пакет 
        :param data: данные, полученые по сети
        """
        try:
            # выполняем преобразование данных в пакет БАЗОВОГО ФОРМАТА, для идентификации
            packet = chanel.BaseChanelLevelPacket.from_buffer_copy(data)
        except Exception as e:
            logging.error(str(e))
            return None

        if packet is not None:
            #logging.info('Получен пакет размера: {0} байт'.format(ctypes.sizeof(packet)))
            if SETTINGS['PROTOCOLS']['MAGIC_NUMBER'] == packet.magic_number:
                # Идентифицируем пакет
                if packet.type in self._packets_creators:
                    factory = self._packets_creators[packet.type]['factory']
                    cmd = self._packets_creators[packet.type]['cmd']
                    # Вызываем обработчик и передаем ему "распарсеный" пакет
                    return cmd(packet=factory.factory_method(data))
                else:
                    logging.error('Пакет неизвестного типа!')
            else:
                logging.error('Пакет не имеет магического числа!')
        else:
             logging.error('Пакет не распарсился')
        return None