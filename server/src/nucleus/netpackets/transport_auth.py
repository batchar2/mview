import ctypes

from settings import SETTINGS

"""
Транспортный протокол: авторизация.
Служит для обработкии сообщений авторизации: получение ключей и прочее
"""

class BasePacketAuth(ctypes.LittleEndianStructure):
    # Базовый пакет с общими полями: пакет служит для приведения типов 
    # Данная структура нужна для идентификации ТИПА приходящего пакета.
    
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
    ]


class PacketKeyAuth(ctypes.LittleEndianStructure):
    """
    Данный пакет необходим для авторизации (обмен ключами)
    """
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # размер ключа в поле
        ('length', ctypes.c_uint32, 32),
        # Ключ
        ('key', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['KEY_SIZE'])
    ]


class PacketUserRequestAuth(ctypes.LittleEndianStructure):
    """
    Данный пакет необходим для отправки на сервер идентификаторов пользователя
    """    
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # Тело сообщения (Логин и пароль в зашифрованом виде)
        ('username', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['LOGIN_SIZE']),
        ('password', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['PASSWORD_SIZE']),
    ]


class PacketUserResponseAuth(ctypes.LittleEndianStructure):
    """ 
    Ответ пользователю от сервера о статусе авторизации
    Успех: поля информации о пользователе заполнены.
    type - несет в себе два значения: успешная или нет авторизация.     
    """
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # Id-пользователя
        ('user_id', ctypes.c_uint32, 32),
        # уникальный идентификатор сессии пользователя
        ('user_session_uid', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['UUID_SIZE']),
    ]