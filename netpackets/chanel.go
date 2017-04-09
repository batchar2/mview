package netpackets

import (
	"octopus/conf"
)

type ChanelPacketHeader struct {
	PacketHeader
	body [conf.CHANEL_PACKET_BODY_SIZE]byte
}

func (header *ChanelPacketHeader) SetBody(body []byte) {
	copy(body, header.body[:])
}

func (header *ChanelPacketHeader) GetBody() [conf.CHANEL_PACKET_BODY_SIZE]byte {

	return header.body
}
