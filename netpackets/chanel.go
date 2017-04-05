package netpackets

import (
    "mview/conf"
)

type ChanelPacketHeader struct {
    Header PacketHeader
    body [conf.CHANEL_BODY_SZIE]byte
}

func (header *ChanelPacketHeader) SetBody(body [conf.CHANEL_BODY_SZIE]byte) {
    header.body = body
}

func (header *ChanelPacketHeader) GetBody() [conf.CHANEL_BODY_SZIE]byte {
    return header.body
}