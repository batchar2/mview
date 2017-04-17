// описывается цепочка методов для генерации пакета ответа
package pipeline

import (
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

// Хранит цепочку объязаностей и метод который нужно будет вызвать вконце обработки
type PipelineResponse struct {
	//pipeline *list.List
	pipeline []ResponsePacket
}

// Добавляет обработчик в цепочку
func (self *PipelineResponse) AddItem(item ResponsePacket) {
	if self.pipeline == nil {
		//self.pipeline = make(ResponsePacket)
		//map[uint8]*pipeline.PipelineResponse
	}
	self.pipeline = append(self.pipeline, item) // PushBack(item)
}

// Запускает цепочку на исполнение
func (self *PipelineResponse) Run(data []byte) {
	if self.pipeline != nil {
		var number = 0
		var dataPacket = make([]byte, conf.PACKET_SIZE)
		for _, item := range self.pipeline {
			if number == 0 {
				(item).MakePacket(data)

			} else {
				(item).MakePacket(dataPacket)
			}
			number += 1
			dataPacket = (item).GetBinaryPacketData()
		}
	}

	/*
		var dataPacket = make([]byte, conf.PACKET_SIZE)
		for item := self.pipeline.Front(); item != nil; item = item.Next() {
			// отправляю данные на обработку
			if len(dataPacket) == 0 {
				item.Value.(ResponsePacket).MakePacket(data)
			} else {
				item.Value.(ResponsePacket).MakePacket(dataPacket)
			}
			// сохраняю полученые данные
			dataPacket = item.Value.(ResponsePacket).GetBinaryPacketData()
		}
	*/
}

func Add() {
	var res = ResponseTest{}
	var pipeline = PipelineResponse{}
	//var r = &res
	//	pipeline.AddItem(res.(ResponsePacket))
	pipeline.AddItem(&res)

}
