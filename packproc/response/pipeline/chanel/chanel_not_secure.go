// Постритель не шифрованого пакета
package chanel

import (
	"fmt"
	"octopus/conf"
	"octopus/netpackets"
	"octopus/packproc"
	"octopus/packproc/response/pipeline"
)

type ChanelNotSecurePacketMaker struct {
	pipeline.ResponsePacket

	packet netpackets.ChanelPacketHeader

	SendDataClient packproc.CallbackSetDataAction
}

// собрать пакет из данных
func (self *ChanelNotSecurePacketMaker) MakePacket(data []byte) bool {
	self.packet = netpackets.ChanelPacketHeader{}

	self.packet.SetBody(data)
	self.packet.SetMagicNumber(conf.MAGIC_NUMBER)
	self.packet.SetPacketType(conf.CHANEL_PACKET_TYPE_NOT_SECURE)

	fmt.Println("ChanelNotSecurePacketMaker")

	self.SendDataClient(self.packet.Binary(), 0)

	return false
}

// Получить бинарное представление пакета
func (self *ChanelNotSecurePacketMaker) GetBinaryPacketData() /*bytes.Buffer { */ []byte {
	return self.packet.Binary()
	//return bytes.Buffer{}
}
