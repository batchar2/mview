// Описываю обработку входящий клиента и ядра системы
package processing

import (
	"fmt"
	"octopus/packproc"
)

// Описываю функции обратного вызова
type PacketProcessing struct {
	// Объекты ответственные за прием запроса и генерацию ответа
	requestProcessing  RequestProcessing
	responseProcessing ResponseProcessing
	// Описываю функции обратного вызова
	SaveSessionKey      packproc.CallbackSetDataAction
	SaveClientPublicKey packproc.CallbackSetDataAction

	SendDataClient  packproc.CallbackSetDataAction
	SendDataNucleus packproc.CallbackSetDataAction
	// Зашифровать открытым ключем клиента
	EncryptCleintPublicKey packproc.CallbackProcessingData
	// Расшифровать открытым ключем сервера
	DecryptServerPrivateKey packproc.CallbackProcessingData
	// Кодировать сессионым ключем данные
	EncryptSessionKey packproc.CallbackProcessingData
	// Декодировать сессионым ключем данные
	DecryptSessionKey packproc.CallbackProcessingData
}

func (self *PacketProcessing) Init() {
	// Инициализация приемника пакета
	self.requestProcessing = RequestProcessing{
		SaveSessionKey:      self.SaveSessionKey,
		SaveClientPublicKey: self.SaveClientPublicKey,

		EncryptCleintPublicKey:  self.EncryptCleintPublicKey,
		DecryptServerPrivateKey: self.DecryptServerPrivateKey,
		EncryptSessionKey:       self.EncryptSessionKey,
		DecryptSessionKey:       self.DecryptSessionKey}

	self.requestProcessing.Init()

}

func (self *PacketProcessing) Processing(data []byte, packetType uint8) {
	//var transportPacketBinaryData =
	var transportBinaryPacket, transportPacketType = self.requestProcessing.Processing(data, packetType)

	self.responseProcessing.Processing(transportBinaryPacket, packetType)

	fmt.Println(transportPacketType)
	fmt.Println(transportBinaryPacket)
}
