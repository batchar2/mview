import ctypes
import logging
from abc import ABC, abstractmethod

#from netpackets import nucleus

from factory.base_creator import BaseCreator

"""
Реализация фабричных методов. Данные методы выполняют приведение типа пакета к определенной структуре.
Пакет движется от пользовательских процессов к ядру
"""


class NucleusPacketCreatorNormal(BaseCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('Ядро: NucleusPacketCreatorNormal')
        pass


class NucleusPacketRequestAuth(BaseCreator):
    """  Запрос на авторизацию клиента """
    
    def factory_method(self, data):
        logging.info('Ядро: NucleusPacketRequestAuth')
        return nucleus.NucleusPacketRequestAuth.from_buffer_copy(data)


