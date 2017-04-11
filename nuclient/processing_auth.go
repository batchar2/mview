package nuclient

import (
	"fmt"
	"octopus/conf"
	"octopus/netpackets"
)

type ProcessingAuth struct {
	nuclient *Nuclient
}

func (p *ProcessingAuth) Start(netPacket netpackets.NetworkPacketHeader) {

	// определяю тип пакета. Для этого строю базовый пакет авторизации
	// По заголовкам идентифицирую конкретный пакет авторизации
	var authBasePacket = netpackets.TransportAuthBasePacketHeader{}
	authBasePacket.ParseBinaryData(netPacket.GetBody())
	var packetType = authBasePacket.GetPacketType()

	fmt.Println("processingAuthPacket")

	switch packetType {
	// Получен публичный ключ от клиента
	case conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND:
		p.processingGetPublicKey(netPacket.GetBody())
	// Клиент отправил сессионый ключ
	case conf.TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY:
		fmt.Println("TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY")
	}
}

func (p *ProcessingAuth) processingGetPublicKey(data []byte) {
	fmt.Println("Обрабатываем публичный ключ клиента")
	var authPacket = netpackets.TransportAuthKeyPacketHeader{}
	authPacket.ParseBinaryData(data)
	var packetType = authPacket.GetPacketType()
	fmt.Print("Пакет типа: ")
	fmt.Println(packetType)
}
