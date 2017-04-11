package netpackets

import (
	"encoding/binary"
)

type PacketHeader struct {
	// Магическое число, отличающее пакет от прочего мусора
	magicNumber uint16
	// Весрия протокола
	version uint8
	// Тип принимаемого пакета
	packetType uint8
}

func (header *PacketHeader) SetMagicNumber(magicNumber uint16) {
	header.magicNumber = magicNumber
}

func (header *PacketHeader) GetMagicNumber() uint16 {
	return header.magicNumber
}

func (header *PacketHeader) SetProtocolVersion(version uint8) {
	header.version = version
}

func (header *PacketHeader) GetProtocolVersion() uint8 {
	return header.version
}

func (header *PacketHeader) SetPacketType(packetType uint8) {
	header.packetType = packetType
}

func (header *PacketHeader) GetPacketType() uint8 {
	return header.packetType
}

// преобразует массив данных в представление пакета
func (header *PacketHeader) parseData(buf []byte) {
	var slMagic = []byte{buf[0], buf[1]}
	var slVersion = []byte{0, buf[2]}
	var slPacketType = []byte{0, buf[3]}

	var magicNumber = binary.BigEndian.Uint16(slMagic)
	var packetVersion = binary.BigEndian.Uint16(slVersion)
	var packetType = binary.BigEndian.Uint16(slPacketType)

	header.SetMagicNumber(magicNumber)
	header.SetProtocolVersion(uint8(packetVersion))
	header.SetPacketType(uint8(packetType))
}

// метод реализует парсинг бинарного пакета в соответствующие загловки
func (header *PacketHeader) ParseBinaryData(data []byte) bool {
	header.parseData(data)
	return true
}
