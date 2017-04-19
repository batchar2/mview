// Пакет отвечает за обработку принятых пакетов от пользователя и генерацию ответа

package processing

import (
	"fmt"
	"octopus/conf"
	"octopus/packproc"
	"octopus/packproc/request/actions/chanel"
	"octopus/packproc/request/actions/network"
	"octopus/packproc/request/actions/transport/auth"
	"octopus/packproc/request/flyweight"
)

type RequestProcessing struct {
	// Приспособленый для каждого сетевого уровня
	chanelProcessing    flyweight.FlyweightFactory
	networkProcessing   flyweight.FlyweightFactory
	transportProcessing flyweight.FlyweightFactory
	// Функии обратного вызова
	SaveSessionKey         packproc.CallbackSetDataAction
	SaveClientPublicKey    packproc.CallbackSetDataAction
	EncryptCleintPublicKey packproc.CallbackProcessingData
	// Расшифровать открытым ключем сервера
	DecryptServerPrivateKey packproc.CallbackProcessingData
	// Кодировать сессионым ключем данные
	EncryptSessionKey packproc.CallbackProcessingData
	// Декодировать сессионым ключем данные
	DecryptSessionKey packproc.CallbackProcessingData
}

// Обработчики канального уровня
func (self *RequestProcessing) initChanelProcessing() {

	var ChanelActionNotSecure = chanel.ChanelNotSecureProcessing{}
	var ChanelActionSecurePubKey = chanel.ChanelSecurePubKeyProcessing{
	//EncryptAction: self.EncryptCleintPublicKey
	}

	self.chanelProcessing = flyweight.FlyweightFactory{}
	self.chanelProcessing.SetFlyweight(conf.CHANEL_PACKET_TYPE_NOT_SECURE, &ChanelActionNotSecure)
	self.chanelProcessing.SetFlyweight(conf.CHANEL_PACKET_TYPE_SECURE_PUBLIC_KEY, &ChanelActionSecurePubKey)
}

// Обработчики сетевого уровня
func (self *RequestProcessing) initNetworkProcessing() {

	var NetworkActionAuth = network.NetworkAuthProcessing{}

	self.networkProcessing = flyweight.FlyweightFactory{}
	self.networkProcessing.SetFlyweight(conf.NETWORK_PACKET_TYPE_AUTH, &NetworkActionAuth)
}

// обработчики траспортного уровня авторизации
func (self *RequestProcessing) initTransportProcessing() {
	var AuthGetPublicKey = auth.AuthGetPublicKeyProcessing{
		SaveClientPublicKeyAction: self.SaveClientPublicKey}

	self.transportProcessing = flyweight.FlyweightFactory{}
	self.transportProcessing.SetFlyweight(conf.TRANSPORT_AUTH_PACKET_TYPE_PUBLICKEY_СLIENT2SERVER_SEND, &AuthGetPublicKey)
}

// Инициализация обработчиков
func (self *RequestProcessing) Init() {
	fmt.Println("Init()")

	self.initChanelProcessing()
	self.initNetworkProcessing()
	self.initTransportProcessing()
}

// Запуск процесса идентификации и обработки пакета: возвращает бинарное представление пакета верхнего уровня (транспортного) и номер команды
func (self *RequestProcessing) Processing(data []byte, packetType uint8) ([]byte, uint8) {

	// Обрабатываем данные сететвого уровня
	var chanelAction = worker(&self.chanelProcessing, data, packetType)
	if chanelAction == nil {
		return nil, 0
	}
	// Обрабатываем данные сетевого уровня
	var networkAction = worker(&self.networkProcessing, chanelAction.GetBodyBinaryData(), chanelAction.GetData2PacketHeader().GetPacketType())
	if networkAction == nil {
		return nil, 0
	}
	// Обрабатываем данные транспортного уровня
	var transportAction = worker(&self.transportProcessing, networkAction.GetBodyBinaryData(), networkAction.GetData2PacketHeader().GetPacketType())
	if transportAction == nil {
		return nil, 0
	}

	return transportAction.BinaryData(), transportAction.GetData2PacketHeader().GetPacketType()
}

// обрабтка данных: поиск оработчика и контроль за получением результата
func worker(factory *flyweight.FlyweightFactory, data []byte, packetType uint8) flyweight.Flyweight {
	//fmt.Printf("PACKET_TYPE_WORKER = %d\n", packetType)
	//fmt.Println(data)
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
