package netpackets

import (
	"octopus/conf"
)

type NetworkPacketHeader struct {
	PacketHeader
	// Тело сообщения (может быть зашифровано)
	body [conf.NETWORK_PACKET_BODY_SIZE]byte
}

func (header *NetworkPacketHeader) SetBody(body []byte) {
	copy(header.body[:], body)
}

func (header *NetworkPacketHeader) GetBody() []byte {
	return header.body[:]
}
