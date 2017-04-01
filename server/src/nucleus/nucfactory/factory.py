"""
Реализуется паттерн "Фабричный метод".
Обрабатывается ядром системы
"""

class PacketCreator(ABC):
    """ Базовый класс создателя продукта """
    @abstractmethod
    def factory_method(self, data):
        """ Фабричный метод, приводит набор данных к соответствующей струтуре
        :param data: данные, полученые от пользователя 
        """
        pass


class PacketCreatorNormal(PacketCreator):
    """  Создатель "нормального пакета" """
    
    def factory_method(self, data):
        logging.info('Пакет определен как PACKET_TYPE_NORMAL')
        pass


class PacketCreatorAuth(PacketCreator):
    """  Запрос на авторизацию клиента """
    
    def factory_method(self, data):
        pass
