// Построитель пакета для авторизации
package network

import (
	"fmt"
	"octopus/conf"
	"octopus/netpackets"
	"octopus/packproc/response/pipeline"
)

type NetworkAuthPacketMaker struct {
	pipeline.ResponsePacket

	packet netpackets.NetworkPacketHeader
}

// собрать пакет из данных
func (self *NetworkAuthPacketMaker) MakePacket(data []byte) bool {
	self.packet = netpackets.NetworkPacketHeader{}

	self.packet.SetBody(data)
	self.packet.SetMagicNumber(conf.MAGIC_NUMBER)
	self.packet.SetPacketType(conf.NETWORK_PACKET_TYPE_AUTH)

	fmt.Println("NetworkAuthPacketMaker")

	return false
}

// Получить бинарное представление пакета
func (self *NetworkAuthPacketMaker) GetBinaryPacketData() /*bytes.Buffer { */ []byte {
	return self.packet.Binary()
}
