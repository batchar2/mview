package testclient

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"net"
	"octopus/conf"
	"octopus/netpackets"
)

func SendPackets() {
	var chanelPacket = netpackets.ChanelPacketHeader{}
	var netPacket = netpackets.NetworkPacketHeader{}

	// Формирую сетевой пакет
	netPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	var netPacketBuff = &bytes.Buffer{}
	binary.Write(netPacketBuff, binary.BigEndian, netPacket)
	fmt.Println(netPacketBuff.Bytes())

	//Формирую канальный пакет
	chanelPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	chanelPacket.SetBody(netPacketBuff.Bytes())
	buf := &bytes.Buffer{}
	binary.Write(buf, binary.BigEndian, chanelPacket)

	fmt.Println(buf.Bytes())

	conn, _ := net.Dial("tcp", "127.0.0.1:60001")

	conn.Write(buf.Bytes())

	fmt.Println("Send data")
	//}
}
