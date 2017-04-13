// Реализует обработку не шифрованых пакетов канального уровня

package chanel

import (
	"fmt"
	"octopus/netpackets"
	"octopus/packproc/request/flyweight"
)

type ChanelNotSecureProcessing struct {
	flyweight.Flyweight

	// Заголовок пакета сетевого уровня
	networkHeader netpackets.PacketHeader
	// Сам пакет данных канального уровня
	packet netpackets.ChanelPacketHeader
}

func (self *ChanelNotSecureProcessing) Processing(data []byte) bool {

	fmt.Println("ChanelNotSecureProcessing")
	// Строю пакет канальнго уровня
	self.packet = netpackets.ChanelPacketHeader{}
	if err := self.packet.ParseBinaryData(data); err {
		return true
	}

	// Строю пакет сетевого уровня
	var networkPacket = netpackets.NetworkPacketHeader{}
	networkPacket.ParseBinaryData(self.packet.GetBody())

	self.networkHeader.SetMagicNumber(networkPacket.GetMagicNumber())
	self.networkHeader.SetProtocolVersion(networkPacket.GetProtocolVersion())
	self.networkHeader.SetPacketType(networkPacket.GetPacketType())

	return false
}

func (self *ChanelNotSecureProcessing) GetData2PacketHeader() *netpackets.PacketHeader {
	return &self.networkHeader

}

func (self *ChanelNotSecureProcessing) GetBodyBinaryData() []byte {
	return self.packet.GetBody()
}

func (self *ChanelNotSecureProcessing) BinaryData() []byte {
	return nil
}
