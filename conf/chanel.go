package conf

const (
	// версия протокола
	CHANEL_PACKET_VERSION uint8 = 1
	// размер поля пакета (складывается из общего размера минус размер полей пакета)
	CHANEL_PACKET_BODY_SIZE uint = PACKET_SIZE - 8

	// пакет зашифрован открытым ключем сервера
	CHANEL_PACKET_TYPE_SECURE_PUBLIC_KEY uint8 = 1
	// пакет зашифрован симметричным ключем
	CHANEL_PACKET_TYPE_SECURE_SIMMETRIC_KEY uint8 = 2
	// пакет не зашифрован (применяется только при обмене ключами)
	CHANEL_PACKET_TYPE_NOT_SECURE uint8 = 3
)
