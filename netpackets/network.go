package netpackets

import (
	"octopus/conf"
)

type NetworkPacketHeader struct {
	PacketHeader
	// Тело сообщения (может быть зашифровано)
	body [conf.NETWORK_PACKET_BODY_SIZE]byte
}

func (header *NetworkPacketHeader) SetBody(body [conf.NETWORK_PACKET_BODY_SIZE]byte) {
	header.body = body
}

func (header *NetworkPacketHeader) GetBody() [conf.NETWORK_PACKET_BODY_SIZE]byte {
	return header.body
}
