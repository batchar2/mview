import logging

from factory.base_action import BaseAction
from cubytes import str2cubytes, cubutes2str


from settings import SETTINGS


"""
Обработчики транспортного протокола авторизации
"""



class ActionTransportAuthGetPublicKey(BaseAction):
    """  Обрабатываем получение симметричного ключа клиента """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketRoute')
        return packet


class ActionTransportAuthGetSessionKey(BaseAction):
    """  Обрабатываем получение сессионого симетричного ключа от клиента """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketAuth')
        return packet


class ActionTransportAuthGetLoginPassword(BaseAction):
    """  Получаем логин и пароль от пользователя """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketAuth')
        return packet
