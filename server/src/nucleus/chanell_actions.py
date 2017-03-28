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



class ActionTypeNormal(Action):
    """  Обработка "нормального"" пакета """
    def __init__(self, *, related_object=None):
        super(ActionTypeNormal, self).__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('Обрабатываем данный пакет ActionTypeNormal. Хочу преобразовать в сетевой')


class ActionTypeQOS(Action):
    """  Обработка "нормального" пакета """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        pass



class ActionTypeClientSendPublicKey(Action):
    """  Обработка пакета с публичным ключем клиента """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        pass