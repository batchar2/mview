package netpackets

// Пакет авторизации, содержит ключ

import (
	"bytes"
	"encoding/binary"
	"octopus/conf"
)

// Конкретный тип данных - отправка ключа
type TransportAuthKeyPacketHeader struct {
	PacketHeader
	// Размер ключа
	keyLength uint32
	// ключ
	key [conf.TRANSPORT_AUTH_KEY_SIZE]byte
	//  поле, которое не используется
	tmp_body [conf.TRANSPORT_AUTH_BASE_PACKET_BODY_SIZE - 4 - conf.TRANSPORT_AUTH_KEY_SIZE]byte
}

func (header *TransportAuthKeyPacketHeader) ParseBinaryData(data []byte) bool {

	header.parseData(data)
	var slKeyLength = data[4:8]

	var keyLength = binary.BigEndian.Uint32(slKeyLength)
	header.SetKeyLength(keyLength)
	if header.keyLength > 0 && header.keyLength < conf.TRANSPORT_AUTH_KEY_SIZE {
		header.SetKey(data[8:header.keyLength])
		return true
	}
	return false
}

// переводит пакет в бинарное представление
func (header *TransportAuthKeyPacketHeader) Binary() []byte {
	var authPacketBuff = &bytes.Buffer{}
	binary.Write(authPacketBuff, binary.BigEndian, *header)
	return authPacketBuff.Bytes()[:]
}

func (header *TransportAuthKeyPacketHeader) SetKey(data []byte) {
	copy(header.key[:], data)
}

func (header *TransportAuthKeyPacketHeader) GetKey() []byte {
	return header.key[:]
}

func (header *TransportAuthKeyPacketHeader) SetKeyLength(length uint32) {
	header.keyLength = length
}

func (header *TransportAuthKeyPacketHeader) GetKeyLenght() uint32 {
	return header.keyLength
}
