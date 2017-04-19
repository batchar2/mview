package testclient

import (
	//"bytes"
	//"encoding/binary"
	"fmt"
	"net"
	"octopus/conf"
	"octopus/netpackets"
)

func SendPackets() {
	// Формирую пакет авторизации
	var authPacket = netpackets.TransportAuthKeyPacketHeader{}
	authPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	authPacket.SetPacketType(conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND)

	// Формирую сетевой пакет
	var netPacket = netpackets.NetworkPacketHeader{}

	netPacket.SetPacketType(conf.NETWORK_PACKET_TYPE_AUTH)
	netPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	netPacket.SetBody(authPacket.Binary())

	//Формирую канальный пакет
	var chanelPacket = netpackets.ChanelPacketHeader{}

	chanelPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	chanelPacket.SetBody(netPacket.Binary())
	chanelPacket.SetPacketType(conf.CHANEL_PACKET_TYPE_NOT_SECURE)

	fmt.Println(chanelPacket.Binary())

	conn, _ := net.Dial("tcp", "127.0.0.1:60001")

	var length = len(chanelPacket.Binary())

	fmt.Println(length)

	conn.Write(chanelPacket.Binary())

	var buf = make([]byte, conf.PACKET_SIZE)
	conn.Read(buf)
	fmt.Println("---------")
	fmt.Println(buf)
}
