// Обрабтчик пакетов
package packproc

import (
	"fmt"
	"octopus/packproc/request"
)

type PacketProcessing struct {
	requestProcessing request.Request
}

func (self *PacketProcessing) Init() {
	// Инициализация приемника пакета
	self.requestProcessing = request.Request{}

	self.requestProcessing.Init()

}

func (self *PacketProcessing) Processing(data []byte, packetType uint8) {
	//var transportPacketBinaryData =
	var transportBinaryPacket, transportPacketType = self.requestProcessing.Processing(data, packetType)

	fmt.Println(transportPacketType)
	fmt.Println(transportBinaryPacket)
}
