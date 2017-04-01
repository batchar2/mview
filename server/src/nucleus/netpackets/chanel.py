import ctypes

from abc import ABCMeta, abstractmethod

from settings import SETTINGS

"""
1. Канальный
Описание структуры сетевых пакетов канального уровня


Пакет канального уровня: в него оборачиваются все данные. Имеет два состояние: авторизация и обмен даннымим

служит для возможности доставки информации от клиента к серверу
"""


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
        ('body', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['PACKET_SIZE'])
    ]



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Дальше обрезаем













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
        ('key', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['KEY_SIZE'])
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
        ('username', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['LOGIN_SIZE']),
        ('password', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['PASSWORD_SIZE']),
    ]