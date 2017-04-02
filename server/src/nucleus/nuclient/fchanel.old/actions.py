import ctypes
import logging

from abc import ABC, abstractmethod

from netpackets import chanel
from netpackets import nucleus

from factory.base_action import BaseAction

from cubytes import str2cubytes, cubutes2str


from settings import SETTINGS

class ActionNormal(BaseAction):
    """  Обработка "нормального"" пакета """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('Обрабатываем данный пакет ActionTypeNormal. Хочу преобразовать в сетевой')


class ActionQOS(BaseAction):
    """  Обработка "нормального" пакета """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        pass



class ActionClientSendPublicKey(BaseAction):
    """  Обработка пакета с публичным ключем клиента """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        """ Получаю от клиента открытый ключ, и генерирую свой """

        settings = self.related_object.settings['PROTOCOLS']
        
        """ self.related_object.set_client_public_key(key=packet.key) """
        self.related_object.generate_rsa_keys()
        
        public_key = self.related_object.get_public_key()

        # строку в массив байт
        
        str2cubytes = lambda s, size: ctypes.cast(s, ctypes.POINTER(ctypes.c_ubyte * size))[0]

        ans_packet = chanel.ChanelLevelPacketKeyAuth()
        ans_packet.magic_number = settings['MAGIC_NUMBER']
        ans_packet.version = settings['CHANEL']['PROTOCOL']['PACKET_VERSION']
        ans_packet.type = settings['CHANEL']['PROTOCOL']['PACKET_TYPE_PUBLIC_KEY_SERVER_CLIENT_EXCHANGE']
        #ans_packet.key = str2cubytes(public_key, op.CHANEL_PACKET_AUTH_BODY_SIZE) 
        ans_packet.length = len(public_key)


        self.related_object.send_user(packet=ans_packet)
        self.related_object.send_user(packet=ans_packet)
        


class ActionClientSendPrivateKey(BaseAction):
    """  Обработка пакета с закрытым симетричным ключем клиента. Зашифрован открытым ключем сервера """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)


    def __call__(self, *, packet=None):
        """ Получаю от клиента пакет.
            Расшифровываю своим закрытым ключем
            Сохраняю секретный симетричный ключ клиента
        """
        settings = self.related_object.settings['PROTOCOLS']

        #data = self.related_object.decode_rsa_data(data=packet.key)
        #self.related_object.set_client_aes_key(key=packet.key)
        data = self.related_object.decode_rsa_data(data=None)
        self.related_object.set_client_aes_key(key=None)

        # Отвечаю клиенту на принятие данных
        ans_packet = chanel.ChanelLevelPacketKeyAuth()
        ans_packet.magic_number = settings['MAGIC_NUMBER']
        ans_packet.version = settings['CHANEL']['PROTOCOL']['PACKET_VERSION']
        ans_packet.type = settings['CHANEL']['PROTOCOL']['PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS']

        self.related_object.send_user(packet=ans_packet)


class ActionClientAuth(BaseAction):
    """ Принятие логина и пароля от пользователя.
        Зашифрованы симетричным ключем
    """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        """ Получаю от клиента пакет.
            Расшифровываю симетричным ключем
            Отправляю ядру на верификацию
            Ответ придет позже, асинхронно (еще не сделано)
        """
        settings = self.related_object.settings['PROTOCOLS']

        username = cubutes2str(packet.username)
        password = cubutes2str(packet.password)

        logging.info('Клиент получил логин и пароль пользователя: {0}  {1}'.format(username, password))
        
        nuc_packet = nucleus.NucleusPacketRequestAuth()
        nuc_packet.magic_number = settings['MAGIC_NUMBER']
        nuc_packet.version = settings['NUCLEUS']['PROTOCOL']['PACKET_VERSION']
        #nuc_packet.username = str2cubytes(username, SETTINGS['PROTOCOLS']['LOGIN_SIZE']) #packet.username 
        #nuc_packet.password = str2cubytes(password, SETTINGS['PROTOCOLS']['PASSWORD_SIZE']) #packet.password
        
        nuc_packet.username = packet.username 
        nuc_packet.password = packet.password
        

        nuc_packet.type = settings['NUCLEUS']['PROTOCOL']['PACKET_TYPE_AUTORIZATION']
        
        self.related_object.request_nucleus(packet=nuc_packet)
        

        