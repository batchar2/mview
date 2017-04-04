package main


import (
    "mview/nucleus"
)


func main() {
    var ncl = nucleus.Nucleus{Host: "127.0.0.1", Port: "9988", Debug: true}
    ncl.Start()
}