package nucleus

// Ядро сервера: Nucleus

import (
	"fmt"
	"net"
	"octopus/netpackets"
	"octopus/nuclient"
)

type Nucleus struct {
	// Параметры сервера
	Host  string
	Port  string
	Debug bool

	//chanelConnect chan net.Conn
}

func (n *Nucleus) Start() bool {
	// канал связи с горутиной принимающее подключение пользователей
	var chanelConnect = make(chan net.Conn)
	// канал для связи горутины пользователя с ядром системы
	var chanelClient2Nucleus = make(chan netpackets.NetworkPacketHeader, 100)

	// Создаем объект для осуществелния подключения пользователей (нуклиент)
	var cleintConnect = connection{Host: n.Host, Port: n.Port, ConnectChanel: chanelConnect}
	// Запускаем в горутине
	go cleintConnect.Listen()

	for {
		select {
		// получаем из канала сведенья о новом подключении пользователя
		case conn := <-chanelConnect:
			// Создаем объект который будет обслуживать связь с клиентом
			client := nuclient.Nuclient{Connect: conn, ChanelNucleus: chanelClient2Nucleus}
			// Запускаем обслуживание клиента в отдельной горутине
			go client.Start()
		// получаем от нуклиента пакет данных
		case netPacket := <-chanelClient2Nucleus:
			netPacket.GetMagicNumber()
			fmt.Println("Получен пакет от нуклиента")
		}
	}
	return true
}
