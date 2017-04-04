package nucleus

import (
    "fmt"
    "os"
    "net"

    "mview/nuclient"
)

type Nucleus struct {
    Host string
    Port string
    Debug bool
}



func (n *Nucleus) Start() bool {
    
    if n.Debug == true {
        fmt.Println("DEBUG: Port=" + n.Port)
    }

    listenSocket, err := net.Listen("tcp", n.Host+":"+n.Port)
    if err != nil {
        fmt.Println("Error listen!")
        os.Exit(1)
    }
    defer listenSocket.Close()

    for {
        conn, err := listenSocket.Accept()
        if err == nil {
            client := nuclient.Nuclient{}
            go client.Connection(conn)
            //go n.nuclient(conn)
        }
    }

    return false
}