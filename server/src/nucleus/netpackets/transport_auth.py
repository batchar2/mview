import ctypes

from settings import SETTINGS

from cubytes import str2cubytes, cubutes2str


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
        # заполнение буфера
        ('tmp', ctypes.c_ubyte * (SETTINGS['PROTOCOLS']['NETWORK']['BODY_SIZE']-4)),
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
        ('key', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['KEY_SIZE']),

        ('tmp', ctypes.c_ubyte * (SETTINGS['PROTOCOLS']['NETWORK']['BODY_SIZE'] - 8 - SETTINGS['PROTOCOLS']['KEY_SIZE'])),
    ]

    def set_key(self, *, key):
        self.key = (ctypes.c_ubyte * ctypes.sizeof(self.key)).from_buffer_copy(key)


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

        ('tmp', ctypes.c_ubyte * (SETTINGS['PROTOCOLS']['NETWORK']['BODY_SIZE'] - 4 - SETTINGS['PROTOCOLS']['LOGIN_SIZE'] - SETTINGS['PROTOCOLS']['PASSWORD_SIZE']))
    ]

    def set_username(self, *, username):
        self.username = str2cubytes(username, ctypes.sizeof(self.username))#(ctypes.c_ubyte * ctypes.sizeof(self.username)).from_buffer_copy(username)

    def set_password(self, *, password):
        self.password = str2cubytes(password, ctypes.sizeof(self.password))#(ctypes.c_ubyte * ctypes.sizeof(self.password)).from_buffer_copy(password)


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


        ('tmp', ctypes.c_ubyte * (SETTINGS['PROTOCOLS']['NETWORK']['BODY_SIZE'] - 8 - SETTINGS['PROTOCOLS']['UUID_SIZE'])),
    ]

