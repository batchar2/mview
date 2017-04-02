import logging

from factory.base_action import BaseAction
from cubytes import str2cubytes, cubutes2str

from settings import SETTINGS


"""
Задача событий канального уровня: расшифровать пакет и передать дальше по цепочке
"""



class ActionSecurePublicKey(BaseAction):
    """  Пакет зашифрован публичным ключем сервера """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionSecurePublicKey')
        # расшифровываем соедржимое пакета и передаем на обработку сетевому уровню
        self.related_object.network_identity(data=packet.body)
        


class ActionSecureSimmetricKey(BaseAction):
    """  Пакет зашифрован симметричным ключем сервера """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionSecureSimmetricKey')
        # расшифровываем соедржимое пакета и передаем на обработку сетевому уровню
        self.related_object.network_identity(data=packet.body)

class ActionNotSecure(BaseAction):
    """  Пакет зашифрован симметричным ключем сервера """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionNotSecure')
        # передаем соедржимое пакета на обработку сетевому уровню
        self.related_object.network_identity(data=packet.body)