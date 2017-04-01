import logging
from abc import ABC, abstractmethod

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


    @property
    def related_object(self):
        return self._related_object


class ActionTypeNormal(Action):
    """ Нормальный пакет. Это данные пользователя. Проверяю сессию и отпускаю """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)


    def __call__(self, *, packet=None):
        logging.info('В ядро пришел нормальный пакет')


class ActionTypeRequestAuth(Action):
    """ Запрос на авторизацию """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)


    def __call__(self, *, packet=None):
        logging.info('В ядро запрос на авторизацию')
