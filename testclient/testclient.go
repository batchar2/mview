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

	chanelPacket.SetMagicNumber(conf.MAGIC_NUMBER)

	conn, _ := net.Dial("tcp", "127.0.0.1:60001")

	buf := &bytes.Buffer{}
	err := binary.Write(buf, binary.BigEndian, chanelPacket)

	fmt.Println(err)
	//for {
	// read in input from stdin
	//reader := bufio.NewReader(os.Stdin)
	//fmt.Print("Text to send: ")
	//text, _ := reader.ReadString('\n')
	// send to socket
	//fmt.Fprintf(conn, text+"\n")
	// listen for reply
	//message, _ := bufio.NewReader(conn).ReadString('\n')
	//fmt.Print("Message from server: " + message)

	conn.Write(buf.Bytes())

	fmt.Println("Send data")
	//}
}
