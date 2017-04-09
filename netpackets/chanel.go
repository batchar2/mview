package netpackets

import (
	"octopus/conf"
)

type ChanelPacketHeader struct {
	PacketHeader
	body [conf.CHANEL_PACKET_BODY_SIZE]byte
}

func (header *ChanelPacketHeader) SetBody(body []byte) {
	copy(header.body[:], body)
}

func (header *ChanelPacketHeader) GetBody() []byte {

	return header.body[:]
}
