// Получаем публичный ключ от пользователя
package auth

import (
	"fmt"
	"octopus/netpackets"
	"octopus/packproc"
	"octopus/packproc/request/flyweight"
)

type AuthGetSessionKeyProcessing struct {
	flyweight.Flyweight

	packet netpackets.TransportAuthKeyPacketHeader

	header netpackets.PacketHeader
	// Сохранить сессионый ключ
	SaveSessionKey packproc.CallbackSetDataAction
}

func (self *AuthGetSessionKeyProcessing) Processing(data []byte) bool {

	fmt.Println("AuthGetSessionKeyProcessing")
	self.packet = netpackets.TransportAuthKeyPacketHeader{}
	if err := self.packet.ParseBinaryData(data); err {
		return true
	}

	self.header = netpackets.PacketHeader{}
	self.header.SetMagicNumber(self.packet.GetMagicNumber())
	self.header.SetPacketType(self.packet.GetPacketType())

	self.SaveSessionKey(self.packet.GetKey(), self.packet.GetKeyLenght())

	return false
}

func (self *AuthGetSessionKeyProcessing) GetData2PacketHeader() *netpackets.PacketHeader {
	return &self.header

}

func (self *AuthGetSessionKeyProcessing) GetBodyBinaryData() []byte {
	return nil
}

func (self *AuthGetSessionKeyProcessing) BinaryData() []byte {
	return self.packet.Binary()
}
