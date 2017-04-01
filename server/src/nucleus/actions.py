import logging
from abc import ABC, abstractmethod

from factory.base_action import BaseAction



class ActionTypeNormal(BaseAction):
    """ Нормальный пакет. Это данные пользователя. Проверяю сессию и отпускаю """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)


    def __call__(self, *, packet=None):
        logging.info('В ядро пришел нормальный пакет')



class ActionTypeRequestAuth(BaseAction):
    """ Запрос на авторизацию """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)


    def __call__(self, *, packet=None):
        logging.info('В ядро запрос на авторизацию')
