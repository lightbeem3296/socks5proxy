package main

import (
	"flag"
	"fmt"

	"github.com/armon/go-socks5"
)

func main() {
	// Define the port flag
	port := flag.String("port", "8000", "port to listen on for the SOCKS5 proxy")
	flag.Parse()

	// Create a SOCKS5 server
	conf := &socks5.Config{}
	server, err := socks5.New(conf)
	if err != nil {
		panic(err)
	}

	// Start the SOCKS5 proxy on the specified port
	address := fmt.Sprintf("127.0.0.1:%s", *port)
	if err := server.ListenAndServe("tcp", address); err != nil {
		panic(err)
	}
}
