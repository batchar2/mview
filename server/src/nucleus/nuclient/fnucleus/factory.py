# фабрика идентификатоции типа пакета от ядра
import ctypes
import logging

from abc import ABC, abstractmethod


from netpackets import chanel 


class PacketCreator(ABC):
    """ Базовый класс создателя продукта """
    @abstractmethod
    def factory_method(self, data):
        """ Фабричный метод, приводит набор данных к соответствующей струтуре
        :param data: данные, полученые от пользователя 
        """
        pass


class NucleusPacketCreatorAuthRespnse(PacketCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('ОТВЕТ ОТ ЯДРА АВТОРИЗАЦИЯ')
        return chanel.ChanelLevelPacket.from_buffer_copy(data)