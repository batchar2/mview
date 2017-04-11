package netpackets

import (
	"bytes"
	"encoding/binary"
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

// метод реализует парсинг бинарного пакета в соответствующие загловки
func (header *NetworkPacketHeader) ParseBinaryData(data []byte) bool {
	header.parseData(data)
	header.SetBody(data[4:])
	return true
}

// переводит пакет в бинарное представление
func (header *NetworkPacketHeader) Binary() []byte {
	var authPacketBuff = &bytes.Buffer{}
	binary.Write(authPacketBuff, binary.BigEndian, *header)
	return authPacketBuff.Bytes()[:]
}
