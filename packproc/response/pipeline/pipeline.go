// описывается цепочка методов для генерации пакета ответа
package pipeline

import (
	"fmt"
	//"bytes"
	//"container/list"
	"octopus/conf"
)

// Интерейс для приспособленцев
type ResponsePacket interface {
	// собрать пакет из данных
	MakePacket(data []byte) bool
	// Получить бинарное представление пакета
	GetBinaryPacketData() []byte // bytes.Buffer
}

/*
type ResponseTest struct {
}

// собрать пакет из данных
func (self *ResponseTest) MakePacket(data []byte) bool {

	return false
}

// Получить бинарное представление пакета
func (self *ResponseTest) GetBinaryPacketData() []byte {
	return nil //bytes.Buffer{}
}
*/
// Хранит цепочку объязаностей и метод который нужно будет вызвать вконце обработки
type PipelineResponse struct {
	//pipeline *list.List
	pipeline []ResponsePacket
}

// Добавляет обработчик в цепочку
func (self *PipelineResponse) AddItem(item ResponsePacket) {
	self.pipeline = append(self.pipeline, item) // PushBack(item)

	fmt.Println(len(self.pipeline))
}

// Запускает цепочку на исполнение
func (self *PipelineResponse) Run(data []byte) {
	var dataPacket = make([]byte, conf.PACKET_SIZE)
	for i, item := range self.pipeline {
		if i == 0 {
			item.MakePacket(data)

		} else {
			item.MakePacket(dataPacket)
		}
		dataPacket = item.GetBinaryPacketData()
		//fmt.Println("----")
		//fmt.Println(i)
		//fmt.Println(dataPacket)
	}
}
