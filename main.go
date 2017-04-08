package main

import (
	"fmt"
	"octopus/nucleus"
	"octopus/testclient"
	"os"
)

func main() {

	if len(os.Args) == 1 {
		fmt.Println("Start server")
		var nucl = nucleus.Nucleus{Host: "127.0.0.1", Port: "60001", Debug: true}
		nucl.Start()
	} else {
		testclient.SendPackets()
	}
}
