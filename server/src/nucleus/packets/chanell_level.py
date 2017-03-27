import ctypes

from abc import ABCMeta, abstractmethod

from  default_options import CHANEL_PACKET_BODY_SIZE


"""
class ChanelState(metaclass=ABCMeta):

    _data = None
    def __init__(self, data_buf):
        self._data = data_buf

    @abstractmethod
    def __call__(self, callback):
        pass

    @property
    def data(self):
        return self._data


class ChanelGetPublicKeyClientState(ChanelState):
    
    def __init__(self, data_buf):
        super().__init__(data_buf)


class ChanelSendPublicKeyServerState(ChanelState):
    
    def __init__(self, data_buf):
        super().__init__(data_buf)

"""

class ChanelLevelPacket(ctypes.LittleEndianStructure):
    """ Структура пакета канального уровня """
    
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32)
        # ip-адрес клиента
        ('body', ctypes.c_ubyte * CHANEL_PACKET_BODY_SIZE),
    ]