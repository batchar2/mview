// описывается цепочка методов для генерации пакета ответа
package pipeline

import (
	"container/list"
)

// Интерейс для приспособленцев
type Response interface {
	// собрать пакет из данных
	//MakePacket(data []byte) bool
	// Получить бинарное представление пакета
	//GetBinaryPacketData() []byte
}

/*
type ResponseTest struct {
	Response
}

// собрать пакет из данных
func (self *ResponseTest) MakePacket(data []byte) bool {

	return false
}

// Получить бинарное представление пакета
func (self *ResponseTest) GetBinaryPacketData() []byte {
	return nil
}
*/
// Хранит цепочку объязаностей и метод который нужно будет вызвать вконце обработки
type PipelineResponse struct {
	pipeline list.List
}

// Добавляет обработчик в цепочку
func (self *PipelineResponse) AddItem(item Response) {
	//self.pipeline.PushBack(item)
}

// Запускает цепочку на исполнение
func (self *PipelineResponse) Run(data []byte) {
	/*
		for item := self.pipeline.Front(); item != nil; item = item.Next() {
			// отправляю данные на обработку
			//item.Value.(Response).MakePacket(data)
			// сохраняю полученые данные
			//var data = item.Value.(Response).GetBinaryPacketData()
		}
	*/
}
