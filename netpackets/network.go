package netpackets

import (
    "mview/conf"
)

type NetworkPacketHeader struct {
    // Магическое число, отличающее пакет от прочего мусора
    magicNumber uint16
    // Весрия протокола
    version uint8
    // Тип принимаемого пакета
    packetType uint8
    // Тело сообщения (может быть зашифровано)
    body [conf.NETWORK_BODY_SZIE]byte
}


func (header *NetworkPacketHeader) SetMeagicNumber(magicNumber uint16) {
    header.magicNumber = magicNumber
}

func (header *NetworkPacketHeader) GetMeagicNumber() uint16 {
    return header.magicNumber
}



func (header *NetworkPacketHeader) SetProtocolVersion(version uint8) {
    header.version = version
}

func (header *NetworkPacketHeader) GetProtocolVersion() uint8 {
    return header.version
}




func (header *NetworkPacketHeader) SetPacketType(packetType uint8) {
    header.packetType = packetType
}

func (header *NetworkPacketHeader) GetPacketType() uint8 {
    return header.packetType
}



func (header *NetworkPacketHeader) SetBody(body [conf.NETWORK_BODY_SZIE]byte) {
    header.body = body
}

func (header *NetworkPacketHeader) GetBody() [conf.NETWORK_BODY_SZIE]byte {
    return header.body
}