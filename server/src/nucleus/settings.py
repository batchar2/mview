"""
Располоджены глобальные опции проекта
"""
import os
import sys

# размер идентификатора пакета
_UUID_SIZE = 16
# размер полей логина и пароля
_LOGIN_PASSOWRD_SIZE = 128

# размер пакета (сетевого - максимальный)
_PACKET_SIZE = 1300

# Размер тела пакета канального уровня
_CHANEL_BODY_SIZE = _PACKET_SIZE - 8
# размер тела пакета сетевого уровня
_NETWORK_BODY_SIZE = _CHANEL_BODY_SIZE - 4

_TRANSPORT_BODY_SIZE = _NETWORK_BODY_SIZE - 4

SETTINGS =  {
    'PROTOCOLS': {
        'MAGIC_NUMBER': 32189,
        'PACKET_SIZE': _PACKET_SIZE,
        'KEY_SIZE': 128,
        'UUID_SIZE': _UUID_SIZE,
        'LOGIN_SIZE':   _LOGIN_PASSOWRD_SIZE,
        'PASSWORD_SIZE': _LOGIN_PASSOWRD_SIZE,

        'CHANEL': {
            # ЗАДАЧА протокола канального уровня: донести сообщение и сообщить зашифрованое оно или нет
            'BODY_SIZE': _CHANEL_BODY_SIZE,
            'PROTOCOL': {
                # магичесоке число для верификации и отличия от муссора
                'PACKET_VERSION': 1,
                # пакет зашифрован открытым ключем сервера
                'TYPE_SECURE_PUBLIC_KEY': 1,
                # пакет зашифрован симметричным ключем
                'TYPE_SECURE_SIMMETRIC_KEY': 2,
                # пакет не зашифрован (применяется только при обмене ключами)
                'TYPE_NOT_SECURE': 3,
            }
        },
        'CHANEL_NUCLEUS': {
            # Пакет между ядром и нуклиентом, Ничем не отличается от канального уровня (пока-что) 
            'BODY_SIZE': _CHANEL_BODY_SIZE,
            'PROTOCOL': {
                # магичесоке число для верификации и отличия от муссора
                'PACKET_VERSION': 1,
                'TYPE_NOT_SECURE': 4,
            },
        },
        'NETWORK': {
            # задача сетевого протокола идентифицировать свое тело: какому пакету принадлежит: авторизация, обмен
            'BODY_SIZE': _NETWORK_BODY_SIZE,
            'PROTOCOL': {
                # обмен даннымим между клиентами
                'TYPE_PACKET_ROUTE': 11,
                # идентифицирует авторизацию
                'TYPE_AUTHORIZATION': 12,
                'TYPE_QOS': 13,
            },
        },
        'TRANSPORT': {
            # задача транспортных протоколов: корректное поведение под задачи 
            'BODY_SIZE': _TRANSPORT_BODY_SIZE,
            'PROTOCOL' : {
                # транспортный авторизационный протокол
                'AUTH': {
                    # Пользователь подключился и отправил серверу свой открытый ключ (клиент --> сервер)
                    'PUBLIC_KEY_СLIENT2SERVER_SEND': 21,
                    # В ответ сервер высылает свой открытый ключ (сервер --> клиент)
                    'PUBLIC_KEY_SERVER2CLIENT_SEND': 22,
                    # клиент высылает свой закрытый-симметричный ключ серверу. Зашифровано открытым ключем сервера (клиент --> сервер)
                    'SESSION_PRIVATE_KEY': 5,
                    # сервер подтверждает получение ключа (сервер --> клиент)
                    'PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS': 6,
                    # клиент пересылает свой логин и пароль для проведения авторизации (клиент --> сервер)
                    'PACKET_TYPE_AUTORIZATION': 7,
                    # Успешное завершение авторизации (сервер --> клиент)
                    'PACKET_TYPE_AUTORIZATION_SUCCESS': 8,
                    # Авторизация провалилась, ответ (сервер --> клиент)
                    'PACKET_TYPE_AUTORIZATION_FAIL': 9,
                    # Регистрация отправка пользователем своего логина и пароля
                    'PACKET_TYPE_REGISTRSTION': 10,
                    },
                # транспортный маршрутизационный протокол
                'ROUTE': {

                },
            },
        },
    },
    # расположение пакета с описанием сетвых пакетов. Относительный путь
    'PACKET_HEADERS_PAKET_PATH': 'nucleus',
    'DATABASE' : {
        'ENGINE': 'sqlite:///sqlite_database.db',
    }
}
