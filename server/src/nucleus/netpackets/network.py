import ctypes

from settings import SETTINGS

class NetworkMessage(ctypes.LittleEndianStructure):
    """ Обменный пакет: несет информацию о типе пакета: авторизационный, обменный, QOS """
    _fields_ = [
        ('magic_number', ctypes.c_ushort),
        ('version', ctypes.c_ubyte),
        # Тип пакета: авторизационный, обменный, QOS
        ('type', ctypes.c_ubyte),
        # тело сообщения
        ('body', ctypes.c_ubyte * SETTINGS['PROTOCOLS']['NETWORK']['BODY_SIZE'])
    ]

    def set_body(self, data):
        self.body = (ctypes.c_ubyte * ctypes.sizeof(data)).from_buffer_copy(data)