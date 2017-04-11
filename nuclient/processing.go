package nuclient

import (
	"errors"
	"fmt"
	"octopus/conf"
	"octopus/netpackets"
)

type Processing struct {
	nuclient *Nuclient
}

//  Обрабатываем входящий пакет канального уровня
func (p *Processing) Start(chanelPacket netpackets.ChanelPacketHeader) {

	// Обрабатываем сетевой пакет
	var netPacket, err = p.buildNetworkPacket(chanelPacket.GetBody())
	if err != nil {
		fmt.Println(err)
		return
	}

	// выясняю природу пакета
	switch netPacket.GetPacketType() {

	case conf.NETWORK_PACKET_TYPE_AUTH: // авторизационый пакет
		var processingAuth = ProcessingAuth{nuclient: p.nuclient}
		processingAuth.Start(netPacket)

	case conf.NETWORK_PACKET_TYPE_NORMAL: // пакет обмена даннымим между пользователями

	case conf.NETWORK_PACKET_TYPE_QOS: // пакет проверки качества соединения
	}

}

// строю по набору данных сетевой пакет
func (p *Processing) buildNetworkPacket(data []byte) (netpackets.NetworkPacketHeader, error) {

	var netPacket = netpackets.NetworkPacketHeader{}

	netPacket.ParseBinaryData(data)

	if netPacket.GetMagicNumber() != conf.MAGIC_NUMBER {
		fmt.Println("Неверный магический номер")
		return netPacket, errors.New("Undefined magic number")
	}
	return netPacket, nil
}
