// Реализует обработку шифрованых публичным ключем пакетов канального уровня
package chanel

import (
	"octopus/netpackets"
	"octopus/packproc/request/flyweight"
)

// Выполнить операцию с данными
type CallbackProcessingData func(data []byte, length int) ([]byte, int)

// Реализует обработку  и приведение типов пакетов канального уровня
// Предварительно расшифровав зашифрованый текст
type ChanelSecurePubKeyProcessing struct {
	flyweight.Flyweight

	packet netpackets.PacketHeader

	EncryptAction CallbackProcessingData
}

func (self *ChanelSecurePubKeyProcessing) Processing(data []byte) bool {
	return false
}

func (self *ChanelSecurePubKeyProcessing) GetData2PacketHeader() *netpackets.PacketHeader {
	return &self.packet
}

func (self *ChanelSecurePubKeyProcessing) GetBodyBinaryData() []byte {
	return nil
}

func (self *ChanelSecurePubKeyProcessing) BinaryData() []byte {
	return nil
}
