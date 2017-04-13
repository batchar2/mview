package netpackets

import (
	"bytes"
	"encoding/binary"
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

// метод реализует парсинг бинарного пакета в соответствующие загловки
func (header *ChanelPacketHeader) ParseBinaryData(data []byte) bool {
	//fmt.Println(data)
	header.parseData(data)
	header.SetBody(data[4:])

	if header.GetMagicNumber() != conf.MAGIC_NUMBER {
		return true
	}
	return false
}

// переводит пакет в бинарное представление
func (header *ChanelPacketHeader) Binary() []byte {
	var authPacketBuff = &bytes.Buffer{}
	binary.Write(authPacketBuff, binary.BigEndian, *header)
	return authPacketBuff.Bytes()[:]
}
