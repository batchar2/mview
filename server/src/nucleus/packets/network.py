import ctypes


"""
Описание пакетов сетевого уровня
"""

class NetworPacket(ctypes.LittleEndianStructure):
    """ Пакет сетевого обмена информации """
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # ID отправителя
        ('uid_sender', ctypes.c_uint32, 32),
        # ID-получателя
        ('uid_reciver', ctypes.c_uint32, 32),
        # ID-сессии пользователя отправившего сообщение
        ('uuid_session', ctypes.c_ubyte * 16),
           
    ]