package nuclient

import (
	"fmt"
	"net"
	"octopus/conf"
	"octopus/netpackets"
)

type Nuclient struct {
	ChanelNucleus chan netpackets.NetworkPacketHeader
	Connect       net.Conn
}

func (client *Nuclient) Start() {
	defer client.Connect.Close()
	for {
		buf := make([]byte, conf.PACKET_SIZE)

		size, err := client.Connect.Read(buf)
		if err != nil {
			fmt.Println("Error reading")
			break
		} else {

			netPacket := netpackets.NetworkPacketHeader{}

			fmt.Print(string(buf))
			fmt.Println("Получены данные размера:" + string(size))
			client.ChanelNucleus <- netPacket
			client.Connect.Write(buf)
		}
	}
}
