package testclient

import (
	//"bytes"
	//"encoding/binary"
	"fmt"
	"net"
	"octopus/conf"
	"octopus/netpackets"
)

func makeNetPacket() netpackets.NetworkPacketHeader {
	// Формирую сетевой пакет
	var netPacket = netpackets.NetworkPacketHeader{}
	netPacket.SetPacketType(conf.NETWORK_PACKET_TYPE_AUTH)
	netPacket.SetMagicNumber(conf.MAGIC_NUMBER)

	return netPacket
}

func makeChanelPacket() netpackets.ChanelPacketHeader {
	var chanelPacket = netpackets.ChanelPacketHeader{}
	chanelPacket.SetMagicNumber(conf.MAGIC_NUMBER)

	chanelPacket.SetPacketType(conf.CHANEL_PACKET_TYPE_NOT_SECURE)

	return chanelPacket
}

func PublicKey() netpackets.ChanelPacketHeader {
	// Формирую пакет авторизации
	var authPacket = netpackets.TransportAuthKeyPacketHeader{}
	authPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	authPacket.SetPacketType(conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND)

	var netPacket = makeNetPacket()
	netPacket.SetBody(authPacket.Binary())

	var chanelPacket = makeChanelPacket()
	chanelPacket.SetBody(netPacket.Binary())

	return chanelPacket
}

func SessionKey() netpackets.ChanelPacketHeader {
	// Формирую пакет авторизации
	var authPacket = netpackets.TransportAuthKeyPacketHeader{}
	authPacket.SetMagicNumber(conf.MAGIC_NUMBER)
	authPacket.SetPacketType(conf.TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY)

	var netPacket = makeNetPacket()
	netPacket.SetBody(authPacket.Binary())

	var chanelPacket = makeChanelPacket()
	chanelPacket.SetBody(netPacket.Binary())

	return chanelPacket
}

func SendPackets() {

	//Формирую канальный пакет
	conn, _ := net.Dial("tcp", "127.0.0.1:60001")

	fmt.Println("PUBLIC KEY")

	var pubkey = PublicKey()
	conn.Write(pubkey.Binary())

	var buf = make([]byte, conf.PACKET_SIZE)

	fmt.Println("GET PUBLIC KEY")
	conn.Read(buf)
	fmt.Println(buf)

	fmt.Println("SEND SESSION KEY ")

	var sesKey = SessionKey()
	conn.Write(sesKey.Binary())

	fmt.Println("---------")
	fmt.Println(buf)
}
