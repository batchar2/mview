package nuclient

// Нуклиент - отдельная горутина, отвечающая за связь с удаленым сервером.

import (
	"fmt"
	"net"
	"octopus/conf"
	"octopus/netpackets"
	//	"time"
)

type Nuclient struct {
	// Канал связи между нуклиентом и ядром
	ChanelClient2Nucleus chan NucleusPacketHeader
	// Сетевое соединение между нуклиентом и удаленым клиентом
	Connect net.Conn
	// Прямой канал связи между ядром и нуклиентом
	ChanelNucleus2Client chan NucleusPacketHeader
	// уникальный идентификатор Нуклиента. Используется для опознавания ядром системы
	NuclientUuid string
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

			go nuclient.processingChanelPacket(chanelPacket)

			//var magicNumber = chanelPacket.GetMagicNumber()
			//fmt.Println(magicNumber)
			//var packet = NucleusPacketHeader{}
			//nuclient.ChanelClient2Nucleus <- packet
		// Получены данные от ядра системы
		case <-nuclient.ChanelNucleus2Client:
			fmt.Println("Получены данные от ядра системы")
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

// обработка пакета данных, полученый от удаленого пользователя - канальный уровень
func (nuclient *Nuclient) processingChanelPacket(chanelPacket netpackets.ChanelPacketHeader) {
	fmt.Println("Приняли пакет на обработку")

	var netPacket = netpackets.NetworkPacketHeader{}
	netPacket.ParseData(chanelPacket.GetBody())

	if netPacket.GetMagicNumber() != conf.MAGIC_NUMBER {
		fmt.Println("Неверный магический номер")
	} else {
		//fmt.Println("Верно!")
		nuclient.processingNetworkPacket(netPacket)
	}
}

// обработка пакета данных от пользователя - сетевой уровень
func (nuclient *Nuclient) processingNetworkPacket(netPacket netpackets.NetworkPacketHeader) {
	fmt.Println("processingNetworkPacket")
	// определяю по типу пакета его дальнейший обработчик
	var packetType = netPacket.GetPacketType()
	switch packetType {
	// Пакет авторизации. Производим обработку
	case conf.NETWORK_PACKET_TYPE_AUTH:
		processingAuthPacket(nuclient, netPacket.GetBody())
	case conf.NETWORK_PACKET_TYPE_NORMAL:
	case conf.NETWORK_PACKET_TYPE_QOS:
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

		// Произвожу парсинг данных и строю пакет на основе этих данных
		var packet = netpackets.ChanelPacketHeader{}
		packet.ParseData(buf)
		packet.SetBody(buf[4:])
		fmt.Println(buf)
		// Отличаю от мусорных данных и отпарвляю в канал на обработку нуклиенту
		if packet.GetMagicNumber() == conf.MAGIC_NUMBER {
			chanelData <- packet
		}

	}
}
