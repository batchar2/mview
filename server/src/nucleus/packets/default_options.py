""" Описаны опции по-умолчанию для пакетов """


# магичесоке число для верификации и отличия от муссора
MAGIC_NUMBER = 32189

# Размер тела сообщения канального уровня
CHANEL_PACKET_BODY_SIZE = 1352


# Обмен между клиентом и клиентом. Вставляется во все сообщения,
CHANEL_PACKET_TYPE_NORMAL = 1
# Обмен между клиентом и сервером на предмет качества связи
CHANEL_PACKET_TYPE_QOS = 2


# Пользователь подключился и запросил открытый ключ сервера, в ответ выслал свой открытый ключ (клиент --> сервер)
NETWORK_PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE = 21
# В ответ сервер высылает свой открытый ключ (сервер --> клиент)
NETWORK_PACKET_TYPE_PUBLIC_KEY_SERVER_CLIENT_EXCHANGE = 22
# клиент высылает свой закрытый ключ серверу (клиент --> сервер)
NETWORK_PACKET_TYPE_PRIVATE_KEY_EXCHANGE = 23
# сервер подтверждает получение ключа (сервер --> клиент)
NETWORK_PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS = 24
# клиент пересылает свой логин и пароль для проведения авторизации (клиент --> сервер)
NETWORK_PACKET_TYPE_AUTORIZATION = 25
# Успешное завершение авторизации (сервер --> клиент)
NETWORK_PACKET_TYPE_AUTORIZATION_SUCCESS = 26
# Авторизация провалилась, ответ (сервер --> клиент)
NETWORK_PACKET_TYPE_AUTORIZATION_FAIL = 27


