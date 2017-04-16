// Пакет отвечает за отправку данных пользователю
package processing

import (
	//"octopus/conf"
	"octopus/packproc/response/flyweight"
	"octopus/packproc/response/pipeline"
	//"octopus/packproc/response/pipeline/chanel"
	//"octopus/packproc/response/pipeline/network"
	//"octopus/packproc/response/pipeline/transport/auth"
)

type ResponseProcessing struct {
	// цепочки объязаностей через приспособленца
	pipelines flyweight.FlyweightFactory
}

func (self *ResponseProcessing) Init() {

	self.pipelines = flyweight.FlyweightFactory{}

	// Отправка публичного ключа сервера клиенту
	var pipelinePublicKey = pipeline.PipelineResponse{}
	var authSendPublicKey = pipeline.ResponseTest{} //auth.AuthSendPublicKeyPacketMaker{}
	//var networkAuthPacketMaker = network.NetworkAuthPacketMaker{}
	//var chanelPacketMaker = chanel.ChanelNotSecurePacketMaker{}

	pipelinePublicKey.AddItem(authSendPublicKey)
	//pipelinePublicKey.AddItem(networkAuthPacketMaker)
	//pipelinePublicKey.AddItem(chanelPacketMaker)

	//self.pipelines.SetFlyweight(conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND, pipelinePublicKey)
}

func (self *ResponseProcessing) Processing(data []byte, packetType uint8) {

}
