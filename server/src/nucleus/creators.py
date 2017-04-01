import ctypes
import logging
from abc import ABC, abstractmethod

from netpackets import nucleus

from factory.base_creator import BaseCreator

"""
реализация фабричных методов. Дапнные методы выполня.т приведение типа пакета к определенной структуре. Пакет от пользовательских процессов к ядру
"""


class NucleusPacketCreatorNormal(BaseCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('Пакет определен как PACKET_TYPE_NORMAL')
        pass


class NucleusPacketRequestAuth(BaseCreator):
    """  Запрос на авторизацию клиента """
    
    def factory_method(self, data):
        pass

