package nucleus

import (
    "fmt"
    "net"
    "os"
)

type Nucleus struct {
    Host string
    Port string
    Debug bool
}


func (n *Nucleus) nuclient(conn net.Conn) {
    
    for {
        buf := make([]byte, 1024)
        //reqLen, err := conn.Read(buf)
        _, err := conn.Read(buf)

        if err != nil {
            fmt.Println("Error reading:", err.Error())
            conn.Close()
            break
        }
        conn.Write([]byte("Message received."))
    }
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
            go n.nuclient(conn)
        }
    }

    return false
}