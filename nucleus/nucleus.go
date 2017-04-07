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

	// Ждем подключения пользователей
	go listen(n.Host, n.Port, chanelConnect)

	for {
		select {
		// получаем из канала сведенья о новом подключении пользователя
		case conn := <-chanelConnect:
			// Создаем объект который будет обслуживать связь с клиентом
			client := nuclient.Nuclient{Connect: conn, ChanelClient2Nucleus: chanelClient2Nucleus}
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

// Ожидает подключение удаленого клиента и в канале возвращает это подключение
func listen(host string, port string, connectChanel chan<- net.Conn) {
	listener, err := net.Listen("tcp", host+":"+port)
	if err != nil {
		return
	}
	defer listener.Close()

	for {
		// ждем подключение клиентов
		connection, err := listener.Accept()
		if err != nil {
			fmt.Println("Error connection!")
		} else {
			// скидываем полученое подключение в канал
			connectChanel <- connection
		}
	}
}
