package conf

// Настройки протокола авторизации
const (

    AUTH_PACKET_VERSION uint8 = 1

    // клеент высылает свой публичный ключ
    AUTH_TYPE_PUBLIC_KEY_СLIENT2SERVER_SEND uint8 = 21
    // В ответ сервер высылает свой открытый ключ (сервер --> клиент)
    AUTH_TYPE_PUBLIC_KEY_SERVER2CLIENT_SEN uint8 = 22
    // клиент высылает свой закрытый-симметричный ключ серверу. Зашифровано открытым ключем сервера (клиент --> сервер)
    AUTH_TYPE_SESSION_PRIVATE_KEY uint8 = 23
    // сервер подтверждает получение ключа (сервер --> клиент)
    AUTH_TYPE_PACKET_TYPE_PRIVATE_KEY_EXCHANGE_SUCCESS uint8 = 24
    // клиент пересылает свой логин и пароль для проведения авторизации (клиент --> сервер)
    PACKET_TYPE_AUTORIZATION uint8 = 25
    // Успешное завершение авторизации (сервер --> клиент)
    // PACKET_TYPE_AUTORIZATION_SUCCESS': 26,
    // Авторизация провалилась, ответ (сервер --> клиент)
    //PACKET_TYPE_AUTORIZATION_FAIL': 27,
    // Регистрация отправка пользователем своего логина и пароля
    //PACKET_TYPE_REGISTRSTION': 28,
)