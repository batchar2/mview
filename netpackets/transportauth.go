package netpackets

import (
	"octopus/conf"
)

type TransportAuthPacketHeader struct {
	PacketHeader
	// Тело сообщения (может быть зашифровано)
	body [conf.NETWORK_PACKET_BODY_SIZE]byte
}
