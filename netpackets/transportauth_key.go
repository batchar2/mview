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

func (self *TransportAuthKeyPacketHeader) ParseBinaryData(data []byte) bool {

	self.parseData(data)
	var slKeyLength = data[4:8]

	var keyLength = binary.BigEndian.Uint32(slKeyLength)
	self.SetKeyLength(keyLength)
	if self.keyLength > 0 && self.keyLength < conf.TRANSPORT_AUTH_KEY_SIZE {
		self.SetKey(data[8:self.keyLength])
		return true
	}
	return false
}

// переводит пакет в бинарное представление
func (self *TransportAuthKeyPacketHeader) Binary() []byte {
	var authPacketBuff = &bytes.Buffer{}
	binary.Write(authPacketBuff, binary.BigEndian, *self)
	return authPacketBuff.Bytes()[:]
}

func (self *TransportAuthKeyPacketHeader) SetKey(data []byte) {
	copy(self.key[:], data)
}

func (self *TransportAuthKeyPacketHeader) GetKey() []byte {
	return self.key[:]
}

func (self *TransportAuthKeyPacketHeader) SetKeyLength(length uint32) {
	self.keyLength = length
}

func (self *TransportAuthKeyPacketHeader) GetKeyLenght() uint32 {
	return self.keyLength
}
