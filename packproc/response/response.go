// Пакет отвечает за отправку данных пользователю
package response

import (
	"octopus/response/flyweight"
	"octopus/response/pipeline"
)

type Response struct {
	// цепочки объязаностей через приспособленца
	pipelines flyweight.FlyweightFactory
}

func (self *Response) Init() {

	self.pipelines = flyweight.FlyweightFactory{}

}

func (self *Response) Processing(data []byte, packetType uint8) {

}
