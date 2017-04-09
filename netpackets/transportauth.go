package netpackets

import (
	"octopus/conf"
)

// неопределеный пакет авторизации. Сначала приводится к этому типу данных, в последствии к конкретному
type TransportAuthBasePacketHeader struct {
	PacketHeader
	// Размер неидентифицированого пакета авторизации
	body [conf.TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE]byte
}

// Конкретный тип данных - отправка ключа
type TransportAuthKeyPacketHeader struct {
	PacketHeader
	// Размер ключа
	keyLength uint32
	// ключ
	key [conf.TRANSPORT_AUTH_KEY_SIZE]byte
	//  поле, которое не используется
	tmp_body [conf.TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE - 4 - conf.TRANSPORT_AUTH_KEY_SIZE]byte
}

// Конкретный тип данных - отправка данных пользователя
type TransportAuthUserRequestPacketHeader struct {
	PacketHeader
	username [conf.TRANSPORT_AUTH_USERNAME_SIZE]byte
	password [conf.TRANSPORT_AUTH_PASSWORD_SIZE]byte
	// поле, которое не используется
	tmp_body [conf.TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE - 4 - conf.TRANSPORT_AUTH_USERNAME_SIZE - conf.TRANSPORT_AUTH_PASSWORD_SIZE]byte
}

// Конкретный тип данных - ответ на авторизацию пользователя
type TransportAuthUserResponsePacketHeader struct {
	PacketHeader
	userId        uint32
	userSessionId [conf.UUID_SIZE]byte
	// поле, которое не используется
	tmp_body [conf.TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE - 4 - 4 - conf.UUID_SIZE]byte
}
