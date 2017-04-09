package conf

// Общие настройки приложения
const (
	PACKET_SIZE  uint   = 1300
	MAGIC_NUMBER uint16 = 32189
	// Заркыть соединение по присшествию стольких секунда
	CLOSE_CONNECTION_CLIENT_AFTER_SECONDS int = 5
	// Размер уникального номера
	UUID_SIZE = 40
)
