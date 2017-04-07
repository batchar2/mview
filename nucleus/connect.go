package nucleus

import (
	"fmt"
	"net"
)

/*
Принимает подключение клиента и скидывает полученое подключение в канал
*/
type connection struct {
	Host string
	Port string
	// в канал скидывается подключенный клиенский процесс
	ConnectChanel chan net.Conn
}

func (c *connection) Listen() {
	listener, err := net.Listen("tcp", c.Host+":"+c.Port)
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
			c.ConnectChanel <- connection
		}
	}
}
