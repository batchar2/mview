package netpackets

import (
	"octopus/conf"
)

type ChanelPacketHeader struct {
	PacketHeader
	body [conf.CHANEL_PACKET_BODY_SIZE]byte
}

func (header *ChanelPacketHeader) SetBody(body [conf.CHANEL_PACKET_BODY_SIZE]byte) {
	header.body = body
}

func (header *ChanelPacketHeader) GetBody() [conf.CHANEL_PACKET_BODY_SIZE]byte {
	return header.body
}
