package conf

const (
	NETWORK_PACKET_BODY_SIZE = CHANEL_PACKET_BODY_SIZE - 4

	// Сетевой пакет сигнализирующий о авторизации
	NETWORK_PACKET_TYPE_AUTH uint8 = 11
	// Сетевой пакет сигнализирующий о обмене даннымим между пользователями
	NETWORK_PACKET_TYPE_NORMAL uint8 = 12
	// Сетевой пакет сигнализирующий о проверки качества соединения
	NETWORK_PACKET_TYPE_QOS uint8 = 13
)
