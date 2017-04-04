package main


import (
    "mview/logging"
    "mview/nucleus"
    "mview/netpackets"
)


func main() {
    logging.Init()

    logging.Info.Println("Started")
    var ncl = nucleus.Nucleus{Host: "127.0.0.1", Port: "9988", Debug: true}
    
    p := netpackets.ChanelPacketHeader{}
    p.SetMeagicNumber(10)
    
    ncl.Start()
}