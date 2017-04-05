package main


import (
    "mview/logging"
    "mview/nucleus"
    "mview/netpackets"
    "mview/factory"
)


func main() {
    logging.Init()

    logging.Info.Println("Started")
    var ncl = nucleus.Nucleus{Host: "127.0.0.1", Port: "9988", Debug: true}
    
    p := netpackets.ChanelPacketHeader{}
    p.Header.SetMagicNumber(10)
    
    ncl.Start()

    fmethod := factory.FactoryMethod{}
    fmethod.Tmp()

}