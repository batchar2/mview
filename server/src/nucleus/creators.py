import ctypes
import logging
from abc import ABC, abstractmethod

from netpackets import nucleus

from factory.base_creator import BaseCreator

"""
Реализуется паттерн "Фабричный метод".
Обрабатывается ядром системы
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

