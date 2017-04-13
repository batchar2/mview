package flyweight

import (
	//"fmt"
	"octopus/netpackets"
)

// Интерейс для приспособленцев
type Flyweight interface {

	// включает обработку данных
	Processing(data []byte) bool
	// Получить заголовок нового пакета (из body) для дальнейшей идетификации данных
	GetData2PacketHeader() *netpackets.PacketHeader
	// Получить данные полезной нагрузки пакета
	GetBodyBinaryData() []byte
	// Получить бинарное представление пакета
	BinaryData() []byte
}

// Фабрика для создания приспособленцев
type FlyweightFactory struct {
	pool map[uint8]Flyweight
}

// Добавить приспособленца в пул
func (self *FlyweightFactory) GetFlyweight(state uint8) Flyweight {

	if _, ok := self.pool[state]; ok {
		return self.pool[state]
	}
	return nil
}

// Забрать приспособленца из пула
func (self *FlyweightFactory) SetFlyweight(state uint8, object Flyweight) {
	if self.pool == nil {
		self.pool = make(map[uint8]Flyweight)
	}
	self.pool[state] = object
}
