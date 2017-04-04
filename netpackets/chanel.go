package netpackets

import (
    "mview/conf"
)

type ChanelPacketHeader struct {
    // Магическое число, отличающее пакет от прочего мусора
    magicNumber uint16
    // Весрия протокола
    version uint8
    // Тип принимаемого пакета
    packetType uint8
    // Зарезервированое поле
    nullField uint32
    // Тело сообщения (может быть зашифровано)
    body [conf.CHANEL_BODY_SZIE]byte
}


func (header *ChanelPacketHeader) SetMeagicNumber(magicNumber uint16) {
    header.magicNumber = magicNumber
}

func (header *ChanelPacketHeader) GetMeagicNumber() uint16 {
    return header.magicNumber
}



func (header *ChanelPacketHeader) SetProtocolVersion(version uint8) {
    header.version = version
}

func (header *ChanelPacketHeader) GetProtocolVersion() uint8 {
    return header.version
}




func (header *ChanelPacketHeader) SetPacketType(packetType uint8) {
    header.packetType = packetType
}

func (header *ChanelPacketHeader) GetPacketType() uint8 {
    return header.packetType
}



func (header *ChanelPacketHeader) SetBody(body [conf.CHANEL_BODY_SZIE]byte) {
    header.body = body
}

func (header *ChanelPacketHeader) GetBody() [conf.CHANEL_BODY_SZIE]byte {
    return header.body
}