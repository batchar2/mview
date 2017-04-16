package flyweight

import (
	"octopus/packproc/response/pipeline"
)

// Фабрика для создания приспособленцев
type FlyweightFactory struct {
	pool map[uint8]*pipeline.PipelineResponse
}

// Добавить приспособленца в пул
func (self *FlyweightFactory) GetFlyweight(state uint8) *pipeline.PipelineResponse {

	if _, ok := self.pool[state]; ok {
		return self.pool[state]
	}
	return nil
}

// Забрать приспособленца из пула
func (self *FlyweightFactory) SetFlyweight(state uint8, object *pipeline.PipelineResponse) {
	if self.pool == nil {
		self.pool = make(map[uint8]*pipeline.PipelineResponse)
	}
	self.pool[state] = object
}
