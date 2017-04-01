# фабрика идентификации типа пакета от ядра
import ctypes
import logging

from abc import ABC, abstractmethod

from netpackets import chanel 

from factory.base_creator import BaseCreator
from netpackets import nucleus

class CreatorPacketNormal(BaseCreator):
    """  Успешная авторизация """
    
    def factory_method(self, data):
        logging.info('ОТВЕТ ОТ ЯДРА: Обычный пакет от пользователя')
        return nucleus.NucleusPacketResponseAuth.from_buffer_copy(data)


class CreatorPacketAuthRespnseSuccess(BaseCreator):
    """  Успешная авторизация """
    
    def factory_method(self, data):
        logging.info('ОТВЕТ ОТ ЯДРА: АВТОРИЗАЦИЯ УДАЧНАЯ')
        return nucleus.NucleusPacketResponseAuth.from_buffer_copy(data)


class CreatorPacketAuthResponseFail(BaseCreator):
    """  Ошибка при авторизации" """
    
    def factory_method(self, data):
        logging.info('ОТВЕТ ОТ ЯДРА: АВТОРИЗАЦИЯ НЕУДАЧНАЯ')
        return nucleus.NucleusPacketResponseAuth.from_buffer_copy(data)