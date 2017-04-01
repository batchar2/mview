import logging
from abc import ABC, abstractmethod

from factory.base_action import BaseAction

from netpackets import nucleus

"""
обработчик сообщений от клиенских процессов.
"""



from cubytes import str2cubytes, cubutes2str


class ActionTypeNormal(BaseAction):
    """ Нормальный пакет. Это данные пользователя. Проверяю сессию и отпускаю """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):
        logging.info('В ядро пришел нормальный пакет')



class ActionTypeRequestAuth(BaseAction):
    """ Запрос на авторизацию """
    def __init__(self, *, related_object=None):
        super().__init__(related_object=related_object)

    def __call__(self, *, packet=None):

        print(packet.username)
        print(packet.password)


        username = cubutes2str(packet.username)
        password = cubutes2str(packet.password)
        
        session_uid, is_auth = self.related_object.data_base.auth_user(username, password)
        print(session_uid, is_auth)
        logging.info('Ядро получило данные: логин и пароль пользователя - {0} {0}'.format(username, password))

        # Отправляю клиенту сообщение о завершении операции
        packet_response = nucleus.NucleusPacketResponseAuth()

        settings = self.related_object.settings['PROTOCOLS']

        packet_response.magic_number = settings['MAGIC_NUMBER']
        packet_response.version = settings['NUCLEUS']['PROTOCOL']['PACKET_VERSION']

        packet_response.type = settings['NUCLEUS']['PROTOCOL']['PACKET_TYPE_AUTORIZATION_SUCCESS']
        if is_auth is False:
            packet_response.type = settings['NUCLEUS']['PROTOCOL']['PACKET_TYPE_AUTORIZATION_FAIL']


        self.related_object.send_active_nuclient_packet(packet=packet_response)
