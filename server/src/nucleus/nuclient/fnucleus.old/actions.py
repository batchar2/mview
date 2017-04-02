# обработчики событий от ядра
import ctypes
import logging

from abc import ABC, abstractmethod

from netpackets import chanel
from netpackets import nucleus


from factory.base_action import BaseAction


class ActionNormal(BaseAction):
    def __init__(self, *, related_object=None):
        super(ActionNormal, self).__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('Получен пакет от ядра системы пользовательским процессом')



class ActionAuthResponseSucess(BaseAction):
    def __init__(self, *, related_object=None):
        super(ActionAuthResponseSucess, self).__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('Удачная авторизация')


class ActionAuthResponseFail(BaseAction):
    def __init__(self, *, related_object=None):
        super(ActionAuthResponseFail, self).__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('не удачная авторизация')