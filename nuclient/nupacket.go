package nuclient

import (
	"octopus/netpackets"
)

const (
	NU_PACKET_TYPE_AUTH_SEND_LOGIN uint32 = 1
	UUID_SIZE                      uint32 = 40
)

// Структура создана для обмена между нуклиентом и ядром системы. Несет в себе пакет сетевого уровня
type NucleusPacketHeader struct {
	// тип сообщения
	packetType uint32
	// уникальный идентификатор нуклиента
	uuid string
	// Включает в себя сетевой пакет
	netPacket netpackets.NetworkPacketHeader
}

func (header *NucleusPacketHeader) SetNetPacket(packet netpackets.NetworkPacketHeader) {
	header.netPacket = packet
}

func (header *NucleusPacketHeader) GetNetPacket() netpackets.NetworkPacketHeader {
	return header.netPacket
}

func (header *NucleusPacketHeader) SetPacketType(packetType uint32) {
	header.packetType = packetType
}

func (header *NucleusPacketHeader) GetPacketType() uint32 {
	return header.packetType
}

func (header *NucleusPacketHeader) SetUuid(uuid string) {
	header.uuid = uuid
}

func (header *NucleusPacketHeader) GetUuid() string {
	return header.uuid
}
