package nuclient

import (
	"fmt"
	"octopus/conf"
	"octopus/netpackets"
)

type ProcessingAuth struct {
	nuclient *Nuclient
}

// определяю тип пакета. Для этого строю базовый пакет авторизации
// По заголовкам идентифицирую конкретный пакет авторизации
// Переадаю на обработку фабрике
type ActionMethod func(data []byte)

func (p *ProcessingAuth) Start(netPacket netpackets.NetworkPacketHeader) {

	// Регистрирую обработчики сообщений
	var requestAction = map[uint8]*struct {
		Action ActionMethod
	}{}

	fmt.Println(requestAction)

	requestAction[conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND].Action = p.processingGetPublicKey
	requestAction[conf.TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY].Action = p.processingGetSessionKey

	// Идентифицирую тип пакета. Привожу к базовому пакету авторизации, т.к. заголовик везде одинаковые
	var authBasePacket = netpackets.TransportAuthBasePacketHeader{}
	authBasePacket.ParseBinaryData(netPacket.GetBody())
	var packetType = authBasePacket.GetPacketType()

	// Ищу по типу пакета обработчик и вызываю его
	if value, ok := requestAction[packetType]; ok {
		value.Action(netPacket.GetBody())
	} else {
		fmt.Println("ERROR")
	}
}

func (p *ProcessingAuth) processingGetPublicKey(data []byte) {
	var authPacket = netpackets.TransportAuthKeyPacketHeader{}
	authPacket.ParseBinaryData(data)

	//var packetType = authPacket.GetPacketType()

	//var keyLength = authPacket.GetKeyLenght()

	//	fmt.Print("Пакет типа: ")
	//fmt.Println(packetType)
}

func (p *ProcessingAuth) processingGetSessionKey(data []byte) {
	var authPacket = netpackets.TransportAuthKeyPacketHeader{}
	authPacket.ParseBinaryData(data)

}
