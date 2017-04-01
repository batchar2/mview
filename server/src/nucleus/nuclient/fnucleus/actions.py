# обработчики событий от ядра
import ctypes
import logging

from abc import ABC, abstractmethod

from netpackets import chanel
from netpackets import nucleus

class Action(ABC):
    """ Класс "команда", реализует вызов функции. Используется для связи с клиентом """
    _related_object = None 
    
    def __init__(self, *, related_object=None):
        """
        Конструктор класса, реализует логику обработки пакета
        :param related_object: Ссылка на связанный объект, через который происходит обмен с ядром 
        """
        self._related_object = related_object


    def __call__(self, *, packet=None):
        """
        Вызывается где-то. Таким оразом разделяем логику работу 
        :param packet: тело пакета    
        """
        pass



class NucleusAuthResponse(Action):
        def __init__(self, *, related_object=None):
        super(NucleusAuthResponse, self).__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('Получен пакет от ядра системы')