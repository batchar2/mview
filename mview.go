package main


import (
    "fmt"
    //"watch/nucleus"
)

import nucleus "watch/nucleus"

func main() {
    fmt.Printf("Hello!")
    
    var ncl = nucleus.Nucleus{Host: "127.0.0.1", Port: "9988", Debug: true}
    ncl.Start()
}