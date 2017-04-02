import ctypes

from settings import SETTINGS

class ChanelLevelPacket(ctypes.LittleEndianStructure):
    """ Структура пакета канального уровня. В него оборачиваются все остальные пакеты
    Тип идентифицирует: шифрованое или нет сообщение
    """
    _fields_ = [
        # Магическое число, отличающее пакет от прочего мусора
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        # зашифровано симметричным ключем, зашифровано ассиметричным ключем, не зашифровано 
        ('type', ctypes.c_ubyte),
        # зарезервированное поле
        ('null', ctypes.c_uint32, 32),
        # Тело сообщения (может быть зашифровано)
        ('body', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['CHANEL']['BODY_SIZE'])
    ]
