// Реализует обработку пакетов сетевого уровня, пакеты авторизации
package network

import (
	//"octopus/conf"
	"fmt"
	"octopus/netpackets"
	"octopus/request/flyweight"
)

type NetworkAuthProcessing struct {
	flyweight.Flyweight

	// Заголовок пакета авторизации
	header netpackets.PacketHeader
	// Сам пакет данных сетевого уровня
	packet netpackets.NetworkPacketHeader
}

func (self *NetworkAuthProcessing) Processing(data []byte) bool {

	fmt.Println("NetworkAuthProcessing")
	self.packet = netpackets.NetworkPacketHeader{}
	if err := self.packet.ParseBinaryData(data); err {
		return true
	}

	var transportHeader = netpackets.TransportBasePacketHeader{}
	transportHeader.ParseBinaryData(self.packet.GetBody())

	self.header.SetMagicNumber(transportHeader.GetMagicNumber())
	self.header.SetProtocolVersion(transportHeader.GetProtocolVersion())
	self.header.SetPacketType(transportHeader.GetPacketType())

	return false
}

func (self *NetworkAuthProcessing) GetData2PacketHeader() *netpackets.PacketHeader {
	return &self.header
}

func (self *NetworkAuthProcessing) GetBodyBinaryData() []byte {
	return self.packet.GetBody()
}
