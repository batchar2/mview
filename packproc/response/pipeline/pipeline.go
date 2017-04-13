// описывается цепочка методов для генерации пакета ответа
package pipeline

import (
	"container/list"
)

// Интерейс для приспособленцев
type ResponseInterface interface {

	// собрать пакет из данных
	MakePacket(data []byte) bool
	// Получить бинарное представление пакета
	GetBinaryPacketData() []byte
}

// Хранит цепочку объязаностей и метод который нужно будет вызвать вконце обработки
type PipelineResponse struct {
	pipeline list.List
}

// Добавляет обработчик в цепочку
func (self *PipelineResponse) addItem(item *ResponseInterface) {
	self.pipeline.PushBack(item)
}

// Запускает цепочку на исполнение
func (self *PipelineResponse) Run(data []byte) {

	for item := self.pipeline.Front(); item != nil; item = item.Next() {
		// отправляю данные на обработку
		item.Value.(ResponseInterface).MakePacket(data)
		// сохраняю полученые данные
		data = item.Value.(ResponseInterface).GetBinaryPacketData()
	}
}
