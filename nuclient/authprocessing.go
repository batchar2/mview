package nuclient

// Обработка пакета авторизации от пользователя

import (
	"fmt"
	"octopus/conf"
	"octopus/netpackets"
)

func processingAuthPacket(nuclient *Nuclient, data []byte) {
	// определяю тип пакета. Для этого строю базовый пакет и далее по его заголовкам строю требуемый
	var baseNetPacket = netpackets.TransportAuthBasePacketHeader{}
	baseNetPacket.ParseData(data)
	var packetType = baseNetPacket.GetPacketType()

	fmt.Println("processingAuthPacket")
	fmt.Println(packetType)
	fmt.Println(data)

	switch packetType {
	// Получен публичный ключ от клиента
	case conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND:
		fmt.Println("TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND")
	// Клиент отправил сессионый ключ
	case conf.TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY:
		fmt.Println("TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY")
	}

}
