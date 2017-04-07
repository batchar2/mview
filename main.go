package main

import (
	"fmt"
	"octopus/nucleus"
)

func main() {
	fmt.Println("Start")
	var nucl = nucleus.Nucleus{Host: "127.0.0.1", Port: "60001", Debug: true}
	nucl.Start()
}
