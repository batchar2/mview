""" Описаны опции по-умолчанию для пакетов """


# магичесоке число для верификации и отличия от муссора
MAGIC_NUMBER = 32189
CHANEL_PACKET_VERSION = 1
# Размер тела сообщения канального уровня
CHANEL_PACKET_BODY_SIZE = 1292

# Размер пакет, необходимого для авторизации.
CHANEL_PACKET_AUTH_BODY_SIZE = 60

# Обмен между клиентом и клиентом. Вставляется во все сообщения,
CHANEL_PACKET_TYPE_NORMAL = 1
# Обмен между клиентом и сервером на предмет качества связи
CHANEL_PACKET_TYPE_QOS = 2


# Пользователь подключился и отправил серверу свой открытый ключ (клиент --> сервер)
CHANEL_PACKET_TYPE_PUBLIC_KEY_СLIENT_SERVER_EXCHANGE = 3
# В ответ сервер высылает свой открытый ключ (сервер --> клиент)
CHANEL_PACKET_TYPE_PUBLIC_KEY_SERVER_CLIENT_EXCHANGE = 4
# клиент высылает свой закрытый-симметричный ключ серверу. Зашифровано открытым ключем сервера (клиент --> сервер)
CHANEL_PACKET_TYPE_PRIVATE_KEY_EXCHANGE = 5
# сервер подтверждает получение ключа (сервер --> клиент)
CHANEL_PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS = 6
# клиент пересылает свой логин и пароль для проведения авторизации (клиент --> сервер)
CHANEL_PACKET_TYPE_AUTORIZATION = 7
# Успешное завершение авторизации (сервер --> клиент)
CHANEL_PACKET_TYPE_AUTORIZATION_SUCCESS = 8
# Авторизация провалилась, ответ (сервер --> клиент)
CHANEL_PACKET_TYPE_AUTORIZATION_FAIL = 9


