package conf

// Настройки протокола канального уровня
const (

	CHANEL_PACKET_VERSION uint = 1

	// пакет зашифрован открытым ключем сервера
	CHANEL_TYPE_SECURE_PUBLIC_KEY uint = 1
	// пакет зашифрован симметричным ключем
	CHANEL_TYPE_SECURE_SIMMETRIC_KEY uint = 2
	// пакет не зашифрован (применяется только при обмене ключами)
	CHANEL_TYPE_NOT_SECURE uint = 3
)