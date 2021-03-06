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

	TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND  uint8 = 21
	TRANSPORT_AUTH_PACKET_TYPE_PUBLIC_KEY_SERVER2CLIENT_SEND uint8 = 22
	TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY           uint8 = 23
	// Успешно приняли сессионый ключ от клиента
	TRANSPORT_AUTH_PACKET_TYPE_SESSION_KEY_RESPONSE uint8 = 24
)
