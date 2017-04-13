// Получаем публичный ключ от пользователя
package auth

import (
	"fmt"
	"octopus/netpackets"
	"octopus/request/flyweight"
)

type AuthGetPublicKeyProcessing struct {
	flyweight.Flyweight

	packet netpackets.TransportAuthKeyPacketHeader
}

func (self *AuthGetPublicKeyProcessing) Processing(data []byte) bool {

	fmt.Println("AuthGetPublicKeyProcessing")
	self.packet = netpackets.TransportAuthKeyPacketHeader{}
	if err := self.packet.ParseBinaryData(data); err {
		return true
	}

	return false
}

func (self *AuthGetPublicKeyProcessing) GetData2PacketHeader() *netpackets.PacketHeader {
	return nil

}

func (self *AuthGetPublicKeyProcessing) GetBinaryData() []byte {
	return nil
}
