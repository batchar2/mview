package factory

import (
	"octopus/netpackets"
)

type FactoryMethod struct {
}

func (factory *FactoryMethod) AddAction(packetType uint8, cmd *Action, concreteFactory *Creator) {

}

func (factory *FactoryMethod) Processing(header *netpackets.PacketHeader) *Action {
	return nil
}
