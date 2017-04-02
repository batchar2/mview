import logging

from factory.base_action import BaseAction
from cubytes import str2cubytes, cubutes2str


from settings import SETTINGS

from netpackets.transport_auth import PacketKeyAuth
"""
Обработчики транспортного протокола авторизации
"""



class ActionTransportAuthGetPublicKey(BaseAction):
    """  Обрабатываем получение симметричного ключа клиента """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketRoute')
        client_public_key = packet.key

        protocols = SETTINGS['PROTOCOLS']

        answer_packet = PacketKeyAuth()
        
        packet_type = protocols['TRANSPORT']['PROTOCOL']['AUTH']['PUBLIC_KEY_SERVER2CLIENT_SEND']

        #answer_packet.key = 'Публичный ключ сервера'
        # Отправляю клиенту публичный ключ сервера, шифрую публичным ключем клиента
        answer_packet.type = packet_type
        answer_packet.magic_number = protocols['MAGIC_NUMBER']
            
        self.related_object.make_answer(packet_type=packet_type, packet=answer_packet)
        return packet


class ActionTransportAuthGetSessionKey(BaseAction):
    """  Обрабатываем получение сессионого симетричного ключа от клиента 
        Подтверждаем прием ключа
    """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('ActionPacketAuth')
        
        protocols = SETTINGS['PROTOCOLS']

        answer_packet = PacketKeyAuth()
        
        packet_type = protocols['TRANSPORT']['PROTOCOL']['AUTH']['PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS']

        #answer_packet.key = 'Публичный ключ сервера'
        # Отправляю клиенту публичный ключ сервера, шифрую публичным ключем клиента
        answer_packet.type = packet_type
        answer_packet.magic_number = protocols['MAGIC_NUMBER']
            
        self.related_object.make_answer(packet_type=packet_type, packet=answer_packet)
        return packet


class ActionTransportAuthGetLoginPassword(BaseAction):
    """  Получаем логин и пароль от пользователя """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None, cmd=None):

        logging.info('ActionTransportAuthGetLoginPassword')
