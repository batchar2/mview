package nuclient


import (
    "fmt"
    "net"
)

type Nuclient struct {

}

func (n *Nuclient) Connection(conn net.Conn) {
    for {
        buf := make([]byte, 1024)
        _, err := conn.Read(buf)

        if err != nil {
            fmt.Println("Error reading:", err.Error())
            conn.Close()
            break
        }
        conn.Write([]byte("Message received."))
    }
}
