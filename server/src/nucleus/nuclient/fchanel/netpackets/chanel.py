import ctypes

from abc import ABCMeta, abstractmethod

from .options import CHANEL_PACKET_BODY_SIZE, CHANEL_PACKET_AUTH_BODY_SIZE

#from .. import options

class BaseChanelLevelPacket(ctypes.LittleEndianStructure):
    """ Структура пакета канального уровня. 
        Данная структура нужна для идентификации ТИПА приходящего пакета.
    """
    
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
    ]


class ChanelLevelPacket(ctypes.LittleEndianStructure):
    """ Структура пакета канального уровня. В него оборачиваются все остальные пакеты """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # Тело сообщения
    #    ('body', ctypes.c_ubyte * CHANEL_PACKET_BODY_SIZE)
    ]

    #def __init__(self, body_szie):
    #    self.body


class ChanelLevelPacketKeyAuth(ctypes.LittleEndianStructure):
    """ Структура пакета канального уровня. 
        Данный пакет необходим для авторизации (обмен ключами)
    """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # размер данных
        ('length', ctypes.c_uint32, 32),
        # Тело сообщения (передаеся ключ)
    #    ('key', ctypes.c_ubyte * CHANEL_PACKET_AUTH_BODY_SIZE)
    ]


class ChanelLevelPacketUserAuth(ctypes.LittleEndianStructure):
    """ Структура пакета канального уровня. 
        Данный пакет необходим для авторизации (обмен ключами)
    """
    
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # размер данных
        ('length_username', ctypes.c_ushort),
        ('length_password', ctypes.c_ushort),
        # Тело сообщения (Логин и пароль в зашифрованом виде)
    #    ('username', ctypes.c_ubyte * options.LOGIN_SIZE),
    #    ('password', ctypes.c_ubyte * options.PASSWORD_SIZE),
    ]