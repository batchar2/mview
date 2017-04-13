package netpackets

import (
	"octopus/conf"
)

// Определяю базовый пакет транспортного уровня
type TransportBasePacketHeader struct {
	PacketHeader
	// Размер неидентифицированого пакета авторизации
	body [conf.TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE]byte
}
