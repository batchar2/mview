package request

import (
	"fmt"
	"octopus/conf"
	"octopus/request/flyweight"
	"octopus/request/processing/chanel"
	"octopus/request/processing/network"
	"octopus/request/processing/transport/auth"
)

type Request struct {
	chanelProcessing    flyweight.FlyweightFactory
	networkProcessing   flyweight.FlyweightFactory
	transportProcessing flyweight.FlyweightFactory
}

// Обработчики канального уровня
func (self *Request) initChanelProcessing() {

	var ChanelActionNotSecure = chanel.ChanelNotSecureProcessing{}
	var ChanelActionSecurePubKey = chanel.ChanelSecurePubKeyProcessing{}

	self.chanelProcessing = flyweight.FlyweightFactory{}
	self.chanelProcessing.SetFlyweight(conf.CHANEL_PACKET_TYPE_NOT_SECURE, &ChanelActionNotSecure)
	self.chanelProcessing.SetFlyweight(conf.CHANEL_PACKET_TYPE_SECURE_PUBLIC_KEY, &ChanelActionSecurePubKey)
}

// Обработчики сетевого уровня
func (self *Request) initNetworkProcessing() {

	var NetworkActionAuth = network.NetworkAuthProcessing{}

	self.networkProcessing = flyweight.FlyweightFactory{}
	self.networkProcessing.SetFlyweight(conf.NETWORK_PACKET_TYPE_AUTH, &NetworkActionAuth)
}

// обработчики траспортного уровня авторизации
func (self *Request) initTransportProcessing() {
	var AuthGetPublicKey = auth.AuthGetPublicKeyProcessing{}

	self.transportProcessing = flyweight.FlyweightFactory{}
	self.transportProcessing.SetFlyweight(conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND, &AuthGetPublicKey)
}

// Инициализация обработчиков
func (self *Request) Init() {
	fmt.Println("Init()")

	self.initChanelProcessing()
	self.initNetworkProcessing()
	self.initTransportProcessing()
}

// Запуск процесса идентификации и обработки пакета
func (self *Request) Processing(data []byte, packetType uint8) {

	// Обрабатываем данные сететвого уровня
	var chanelAction = worker(&self.chanelProcessing, data, packetType)
	if chanelAction == nil {
		return
	}
	// Обрабатываем данные сетевого уровня
	var networkAction = worker(&self.networkProcessing, chanelAction.GetBodyBinaryData(), chanelAction.GetData2PacketHeader().GetPacketType())
	if networkAction == nil {
		return
	}
	// Обрабатываем данные транспортного уровня
	var transportAction = worker(&self.transportProcessing, networkAction.GetBodyBinaryData(), networkAction.GetData2PacketHeader().GetPacketType())
	if transportAction == nil {
		return
	}

}

// обрабтка данных: поиск оработчика и контроль за получением результата
func worker(factory *flyweight.FlyweightFactory, data []byte, packetType uint8) flyweight.Flyweight {
	//fmt.Printf("PACKET_TYPE_WORKER = %d\n", packetType)
	fmt.Println(data)
	var action = factory.GetFlyweight(packetType)
	if action != nil {
		if err := action.Processing(data); err {
			return nil
		}
		return action
	}
	fmt.Println("пакет не определен")
	return nil
}
