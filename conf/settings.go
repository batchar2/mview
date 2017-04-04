package conf

// Общие настройки приложения
const (

    PACKET_SIZE uint = 1300

    CHANEL_BODY_SZIE uint = PACKET_SIZE - 8

    NETWORK_BODY_SZIE uint = CHANEL_BODY_SZIE - 4
    MAGIC_NUMBER uint16 = 32189
)