"""
Располоджены глобальные опции проекта
"""
import os
import sys

# размер пакета (сетевого - максимальный)
_PACKET_SIZE = 8 + 1292

SETTINGS =  {
    'PROTOCOLS': {
        'MAGIC_NUMBER': 32189,
        'PACKET_SIZE': _PACKET_SIZE,
        'KEY_SIZE': 128,
        'UUID_SIZE': 32,
        'LOGIN_SIZE':   128,
        'PASSWORD_SIZE': 128,

        'CHANEL': {
            # размер тела пакета канального уровн
            'CHANEL_BODY_SIZE': _PACKET_SIZE - 8,
            'PROTOCOL': {
                # магичесоке число для верификации и отличия от муссора
                'PACKET_VERSION': 1,
                # Размер пакет, необходимого для авторизации.
                'PACKET_AUTH_BODY_SIZE': 600,

                # Обмен между клиентом и клиентом. Вставляется во все сообщения,
                'PACKET_TYPE_NORMAL': 1,
                # Обмен между клиентом и сервером на предмет качества связи
                'PACKET_TYPE_QOS': 2,

                # Пользователь подключился и отправил серверу свой открытый ключ (клиент --> сервер)
                'PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE': 3,
                # В ответ сервер высылает свой открытый ключ (сервер --> клиент)
                'PACKET_TYPE_PUBLIC_KEY_SERVER_CLIENT_EXCHANGE': 4,
                # клиент высылает свой закрытый-симметричный ключ серверу. Зашифровано открытым ключем сервера (клиент --> сервер)
                'PACKET_TYPE_PRIVATE_KEY_EXCHANGE': 5,
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
            }
        },
        'NETWORK': {

        },
        'NUCLEUS': {
            'CHANEL_BODY_SIZE': _PACKET_SIZE - 8,
            'PROTOCOL': {
                'PACKET_VERSION': 1,
                'PACKET_TYPE_NORMAL': 21,
                # клиент пересылает свой логин и пароль для проведения авторизации (клиент --> сервер)
                'PACKET_TYPE_AUTORIZATION': 22,
                # Успешное завершение авторизации (сервер --> клиент)
                'PACKET_TYPE_AUTORIZATION_SUCCESS': 23,
                # Авторизация провалилась, ответ (сервер --> клиент)
                'PACKET_TYPE_AUTORIZATION_FAIL': 24,
            }           
        },
    },
    # расположение пакета с описанием сетвых пакетов. Относительный путь
    'PACKET_HEADERS_PAKET_PATH': 'nucleus',
    'DATABASE' : {
        'ENGINE': 'sqlite:///sqlite_database.db',
    }
}