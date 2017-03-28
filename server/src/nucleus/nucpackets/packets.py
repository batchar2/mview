import ctypes

from . import options as op
"""
Протокол коммуникации клиенских процессов и ядра
"""

from .. import options as base_options

class NuPacket(ctypes.LittleEndianStructure):
    """ Базовый пакет, необходимый для идентификации типа пакета ядром сиситемы """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
    ]


class NuPacketRequestAuth(ctypes.LittleEndianStructure):
    """ Запрос авторизовать пользователя с таким идентификатором """
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
        ('username', ctypes.c_ubyte * base_options.LOGIN_SIZE),
        ('password', ctypes.c_ubyte * base_options.PASSWORD_SIZE),
    ]

class NuPacketResponseAuth(ctypes.LittleEndianStructure):
    """ Ответ ядра на попытку авторизовать пользователя """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # оnтвет сиситемы NUC_AUTH_SUCCESS или NUC_AUTH_FAILED
        ('response', ctypes.c_uint32, 32),
        # идентификатор сессии
        ('uuid', ctypes.c_ubyte * op.NUC_UUID_SIZE),
    ]