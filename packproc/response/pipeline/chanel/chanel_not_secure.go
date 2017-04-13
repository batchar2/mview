// Постритель не шифрованого пакета
package chanel

import (
	"octopus/conf"
	"octopus/netpackets"
	"octopus/response/pipeline"
)

type ChanelNotSecurePacketMaker struct {
	pipeline.ResponseInterface

	packet netpackets.ChanelPacketHeader
}

// собрать пакет из данных
func (self *ChanelNotSecurePacketMaker) MakePacket(data []byte) bool {
	self.packet = netpackets.ChanelPacketHeader{}

	self.packet.SetBody(data)
	self.packet.SetMagicNumber(conf.MAGIC_NUMBER)
	self.packet.SetPacketType(conf.CHANEL_PACKET_TYPE_NOT_SECURE)

	return false
}

// Получить бинарное представление пакета
func (self *ChanelNotSecurePacketMaker) GetBinaryPacketData() []byte {
	return self.packet.Binary()
}
