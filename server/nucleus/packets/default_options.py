""" Описаны опции по-умолчанию для пакетов """


# магичесоке число для верификации и отличия от муссора
MAGIC_NUMBER = 32189

# Размер тела сообщения канального уровня
CHANEL_PACKET_BODY_SIZE = 1352


# Пользователь подключился и запросил открытый ключ сервера, в ответ выслал свой открытый ключ (клиент --> сервер)
CHANEL_PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE = 1
# В ответ сервер высылает свой открытый ключ (сервер --> клиент)
CHANEL_PACKET_TYPE_PUBLIC_KEY_SERVER_CLIENT_EXCHANGE = 2
# клиент высылает свой закрытый ключ серверу (клиент --> сервер)
CHANEL_PACKET_TYPE_PRIVATE_KEY_EXCHANGE = 3
# сервер подтверждает получение ключа (сервер --> клиент)
CHANEL_PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS = 4
# клиент пересылает свой логин и пароль для проведения авторизации (клиент --> сервер)
CHANEL_PACKET_TYPE_AUTORIZATION = 5
# Успешное завершение авторизации (сервер --> клиент)
CHANEL_PACKET_TYPE_AUTORIZATION_SUCCESS = 6
# Авторизация провалилась, ответ (сервер --> клиент)
CHANEL_PACKET_TYPE_AUTORIZATION_FAIL = 7
# Обмен между клиентом и клиентом. Вставляется во все сообщения,
CHANEL_PACKET_TYPE_NORMAL = 8
# Обмен между клиентом и сервером на предмет качества связи
CHANEL_PACKET_TYPE_QOS = 9

