import ctypes

from settings import SETTINGS
"""
Описание пакетов сетевого уровня

2. Сетевой. Имеет два состояния: авторизация и обмен  данными. Пакет отличаются по заголовкам


"""


class BaseNetworkPacket(ctypes.LittleEndianStructure):
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
    ]


class BaseNetworkKeyAuth(ctypes.LittleEndianStructure):
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
    ]




class NetworPacket(ctypes.LittleEndianStructure):
    """ Пакет сетевого обмена информации """
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # ID отправителя
        ('uid_sender', ctypes.c_ubyte, 32),
        # ID-получателя
        ('uid_reciver', ctypes.c_uint32, 32),
        # ID-сессии пользователя отправившего сообщение
        ('uuid_session', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['UUID_SIZE']),
           
    ]


class NetworPacket(ctypes.LittleEndianStructure):
    """ Пакет сетевого обмена информации """
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # ID отправителя
        ('uid_sender', ctypes.c_ubyte, 32),
        # ID-получателя
        ('uid_reciver', ctypes.c_uint32, 32),
        # ID-сессии пользователя отправившего сообщение
        ('uuid_session', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['UUID_SIZE']),
           
    ]