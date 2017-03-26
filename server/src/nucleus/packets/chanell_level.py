import ctypes


from  default_options import CHANEL_PACKET_BODY_SIZE



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