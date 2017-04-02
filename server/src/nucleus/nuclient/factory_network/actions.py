import logging

from factory.base_action import BaseAction
from cubytes import str2cubytes, cubutes2str


from settings import SETTINGS


"""
Задача событий сетевого уровня: задача вызвать обработать пакет в соответствии с типом
"""



class ActionPacketRoute(BaseAction):
    """  Пакет должен быть переслан пользователю """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketRoute')
        return packet


class ActionPacketAuth(BaseAction):
    """  Пакет авторизации """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketAuth')
        return packet


class ActionPacketQOS(BaseAction):
    """  Пакет события проверки качества связи """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketQOS')
        return packet