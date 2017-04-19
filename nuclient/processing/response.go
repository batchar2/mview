// Пакет отвечает за отправку данных пользователю
package processing

import (
	"fmt"
	"octopus/conf"
	"octopus/packproc"
	"octopus/packproc/response/flyweight"
	"octopus/packproc/response/pipeline"
	"octopus/packproc/response/pipeline/chanel"
	"octopus/packproc/response/pipeline/network"
	"octopus/packproc/response/pipeline/transport/auth"
)

type ResponseProcessing struct {
	// цепочки объязаностей через приспособленца
	pipelines flyweight.FlyweightFactory
	// Кодировать сессионым ключем данные
	EncryptSessionKey packproc.CallbackProcessingData
	// Зашифровать открытым ключем клиента
	EncryptCleintPublicKey packproc.CallbackProcessingData
	// отпраука данных
	SendDataClient  packproc.CallbackSetDataAction
	SendDataNucleus packproc.CallbackSetDataAction
}

func (self *ResponseProcessing) Init() {

	self.pipelines = flyweight.FlyweightFactory{}

	// отправка публичного ключа сервера
	var authSendPublicKey = auth.AuthSendPublicKeyPacketMaker{}
	// успешный прием сессионого ключа клиента
	var authSendSuccessReciveSessionKey = auth.AuthSendSessionKeyResponsePacketMaker{}

	var networkAuthPacketMaker = network.NetworkAuthPacketMaker{}
	var chanelPacketMaker = chanel.ChanelNotSecurePacketMaker{
		SendDataClient: self.SendDataClient}

	// Отправка публичного ключа сервера клиенту
	var pipelinePublicKey = pipeline.PipelineResponse{}
	pipelinePublicKey.AddItem(&authSendPublicKey)
	pipelinePublicKey.AddItem(&networkAuthPacketMaker)
	pipelinePublicKey.AddItem(&chanelPacketMaker)

	// отправка подтверждения приема сессионого ключа
	var pipelineSessionResponseKey = pipeline.PipelineResponse{}

	pipelineSessionResponseKey.AddItem(&authSendSuccessReciveSessionKey)
	pipelineSessionResponseKey.AddItem(&networkAuthPacketMaker)
	pipelineSessionResponseKey.AddItem(&chanelPacketMaker)

	self.pipelines.SetFlyweight(conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND, &pipelinePublicKey)
	// ответ на высылку сессионого ключа - подтверждение
	self.pipelines.SetFlyweight(conf.TRANSPORT_AUTH_PACKET_TYPE_SESSION_PRIVATE_KEY, &pipelineSessionResponseKey)
}

func (self *ResponseProcessing) Processing(data []byte, packetType uint8) {
	fmt.Print("PACKET TYPE = ")
	fmt.Println(packetType)
	var pipeline = self.pipelines.GetFlyweight(packetType)
	if pipeline != nil {
		pipeline.Run(data)
	}
}
