package nucleus

// Ядро сервера: Nucleus

import (
	"fmt"
	"net"
	"octopus/nuclient"

	"github.com/satori/go.uuid"
)

type Nucleus struct {
	// Параметры сервера
	Host  string
	Port  string
	Debug bool

	// Канал связи между ядром системы и нуклиентом. Ключем является UUID (нуклиент <-- ядро)
	chanels2nuclient map[string]chan nuclient.NucleusPacketHeader
	// Канал связи между нуклиентом и ядром системы (нуклиент --> ядро)
	chanelClient2Nucleus chan nuclient.NucleusPacketHeader
}

func (n *Nucleus) Start() bool {

	// Инициализирую словарь каналов (от ядра к нуклиенту)
	n.chanels2nuclient = make(map[string]chan nuclient.NucleusPacketHeader)

	// канал для связи горутины пользователя с ядром системы
	n.chanelClient2Nucleus = make(chan nuclient.NucleusPacketHeader, 100)

	// канал связи с горутиной принимающее подключение пользователей
	var chanelConnect = make(chan net.Conn)

	// Ждем подключения пользователей
	go listen(n.Host, n.Port, chanelConnect)

	for {
		select {
		// получаем из канала сведенья о новом подключении пользователя. Создаем горутину-нуклиента
		case conn := <-chanelConnect:
			n.createNuclient(conn)
		// получаем от нуклиента пакет данных
		case <-n.chanelClient2Nucleus:
			//case netPacket := <-n.chanelClient2Nucleus:
			//netPacket.GetMagicNumber()
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

// Функция обеспечивает создание нового нуклиента
func (n *Nucleus) createNuclient(conn net.Conn) {

	// Получаю уникальный идентификатор - назначаю его клиенту
	clientUuid := uuid.NewV4().String()
	fmt.Printf("UUIDv4: %s\n", clientUuid)

	// Создаем канал, который будет обслуживать связь с клиентом
	n.chanels2nuclient[clientUuid] = make(chan nuclient.NucleusPacketHeader)

	var client = nuclient.Nuclient{
		// передаю подключение с удаленым клиентом
		Connect: conn,
		// Передаю канал связи между нуклиентом и ядром системы
		ChanelClient2Nucleus: n.chanelClient2Nucleus,
		// Передаю канал связи между ядром и нуклиетом
		ChanelNucleus2Client: n.chanels2nuclient[clientUuid],
		// Уникальный идентификатор нуклиента
		NuclientUuid: clientUuid}

	// Запускаем обслуживание клиента в отдельной горутине
	go client.Start()
}
