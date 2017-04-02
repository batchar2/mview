import ctypes

from settings import SETTINGS

class ChanelNucleusPacket(ctypes.LittleEndianStructure):
    """ Структура пакета канального уровня между ядром и нуклиентом. В него оборачиваются все остальные пакеты.
        Пока не отличается от пакета канального уровня
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
