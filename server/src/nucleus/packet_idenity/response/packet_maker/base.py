from abc import ABC, abstractmethod


"""
Реализация базового класса - ответчика на сообщения
"""

class BaseResponseMaker(ABC):
    """ Класс "команда", реализует вызов функции. Используется для связи с клиентом """
    
    @abstractmethod
    def run(self, *, packet=None):
        """
        Вызывается где-то. Таким оразом разделяем логику работу 
        :param packet: тело пакета    
        """
        pass
