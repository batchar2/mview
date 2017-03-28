import ctypes

from abc import ABCMeta, abstractmethod

from .default_options import CHANEL_PACKET_BODY_SIZE, CHANEL_PACKET_AUTH_BODY_SIZE


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
        ('body', ctypes.c_ubyte * CHANEL_PACKET_BODY_SIZE)
    ]


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
        ('key', ctypes.c_ubyte * CHANEL_PACKET_AUTH_BODY_SIZE)
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
        ('length', ctypes.c_uint32, 32),
        # Тело сообщения (Логин и пароль в зашифрованом виде)
        ('info', ctypes.c_ubyte * CHANEL_PACKET_AUTH_BODY_SIZE)
    ]