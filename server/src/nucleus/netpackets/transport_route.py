import ctypes

from settings import SETTINGS

class UserPacketRoute(ctypes.LittleEndianStructure):
    """ 
    Обменный пакет: тело пакета шифруется ключами известнымим только пользователям
    """
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        # идентификация типа сообщения между пользователями
        ('type', ctypes.c_ubyte),
        # уникальный идентификатор сессии пользователя - отправителя данных
        ('user_sender_session_uid', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['UUID_SIZE']),
        # шифрованное между пользователями сообщение
        ('body', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['UUID_SIZE'])
    ]