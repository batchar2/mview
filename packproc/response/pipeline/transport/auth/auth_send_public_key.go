// Построитель пакета для авторизации
package auth

import (
	"octopus/conf"
	"octopus/netpackets"
	"octopus/packproc/response/pipeline"
)

type AuthSendPublicKeyPacketMaker struct {
	pipeline.Response

	packet netpackets.NetworkPacketHeader
}

// собрать пакет из данных
func (self *AuthSendPublicKeyPacketMaker) MakePacket(data []byte) bool {
	self.packet = netpackets.NetworkPacketHeader{}

	self.packet.SetBody(data)
	self.packet.SetMagicNumber(conf.MAGIC_NUMBER)
	self.packet.SetPacketType(conf.NETWORK_PACKET_TYPE_AUTH)

	return false
}

// Получить бинарное представление пакета
func (self *AuthSendPublicKeyPacketMaker) GetBinaryPacketData() []byte {
	return self.packet.Binary()
}
