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
	// Формирую пакет авторизации
	var authPacket = netpackets.TransportAuthKeyPacketHeader{}
	authPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	authPacket.SetPacketType(conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND)

	var authPacketBuff = &bytes.Buffer{}
	binary.Write(authPacketBuff, binary.BigEndian, authPacket)
	fmt.Println(authPacketBuff.Bytes())

	// Формирую сетевой пакет
	var netPacket = netpackets.NetworkPacketHeader{}
	netPacket.SetBody(authPacketBuff.Bytes())
	netPacket.SetPacketType(conf.NETWORK_PACKET_TYPE_AUTH)
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
