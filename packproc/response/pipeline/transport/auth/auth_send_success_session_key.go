// Построитель пакета для авторизации
package auth

import (
	//"bytes"
	"fmt"
	"octopus/conf"
	"octopus/netpackets"
	//"octopus/packproc/response/pipeline"
)

type AuthSendSessionKeyResponsePacketMaker struct {
	//pipeline.ResponsePacket

	packet netpackets.TransportAuthKeyPacketHeader
}

// собрать пакет из данных
func (self *AuthSendSessionKeyResponsePacketMaker) MakePacket(data []byte) bool {
	self.packet = netpackets.TransportAuthKeyPacketHeader{}

	//self.packet.SetBody(data)
	self.packet.SetMagicNumber(conf.MAGIC_NUMBER)
	self.packet.SetPacketType(conf.TRANSPORT_AUTH_PACKET_TYPE_SESSION_KEY_RESPONSE)

	fmt.Println("AuthSendSessionKeyResponsePacketMaker")

	return false
}

// Получить бинарное представление пакета
func (self *AuthSendSessionKeyResponsePacketMaker) GetBinaryPacketData() []byte {
	return self.packet.Binary()
}
