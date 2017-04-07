package nuclient

import (
	"fmt"
	"net"
	"octopus/conf"
	"octopus/netpackets"
	//	"time"
)

type Nuclient struct {
	// Канал связи между ядром и нуклиентом
	ChanelClient2Nucleus chan netpackets.NetworkPacketHeader
	// Сетевое соединение между нуклиентом и удаленым клиентом
	Connect net.Conn
}

// Реализация взаимодействия между ядром системы и удаленым клиентом
func (nuclient *Nuclient) Start() {
	defer nuclient.Connect.Close()

	// канал для связи горутины, чтения данных, от клиента до нуклиента
	var chanelClientToNuclient = make(chan netpackets.ChanelPacketHeader, 100)
	// Канал извещает нулиента о завершении работы приложения
	var chanelIsConClose = make(chan bool)
	// Запускаю канал для связи с удаленным клиентом
	go clientReadData(nuclient.Connect, chanelClientToNuclient, chanelIsConClose)

	for {
		select {
		// Получены данные от удаленного клиента
		case chanelPacket := <-chanelClientToNuclient:
			var magicNumber = chanelPacket.GetMagicNumber()
			fmt.Println(magicNumber)

			var netPacket = netpackets.NetworkPacketHeader{}
			nuclient.ChanelClient2Nucleus <- netPacket
		// информировнаие о закрытии соединения с удаленным клиентом
		case <-chanelIsConClose:
			return
			/* закрыть соединение по истечению заданого времени
			case <-time.After(time.Second * conf.CLOSE_CONNECTION_CLIENT_AFTER_SECONDS):
			case <-time.After(time.Second * 5):
				fmt.Println("Время вышло")
				return
			*/
		}
	}
}

// Читаем данные из сокета
func clientReadData(conn net.Conn, chanelData chan<- netpackets.ChanelPacketHeader, chanelIsConClose chan<- bool) {
	for {
		var buf = make([]byte, conf.PACKET_SIZE)
		_, err := conn.Read(buf)
		if err != nil {
			fmt.Println("Сокет закрыт")
			fmt.Print(err)
			chanelIsConClose <- true
			return
		}
		fmt.Print(string(buf))

		var packet = netpackets.ChanelPacketHeader{}
		// отдаем данные нуклиенту
		chanelData <- packet
	}
}
