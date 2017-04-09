package conf

const (
	// Размер поле ключа в пакете
	TRANSPORT_AUTH_KEY_SIZE = 512
	// Размер неидентифицированого пакета авторизации
	TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE = NETWORK_PACKET_BODY_SIZE - 4
	// Размер тела пакета авторизации с ключем (для выравнивания пакета используется)
	//TRANSPORT_AUTH_KEY_BODY_SIZE = TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE - 4 - TRANSPORT_AUTH_KEY_SIZE
	// Размер полей логина и пароля
	TRANSPORT_AUTH_USERNAME_SIZE = 400
	TRANSPORT_AUTH_PASSWORD_SIZE = 400
)
