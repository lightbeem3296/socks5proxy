package main

import (
	"flag"
	"fmt"
	"log"
	"net"

	"github.com/armon/go-socks5"
)

func main() {
	// Define the port flag with a default value of 1080
	port := flag.String("port", "1080", "port to listen on for the SOCKS5 proxy")
	flag.Parse()

	// Logging the start of the server
	log.Printf("Starting SOCKS5 proxy on port %s...\n", *port)

	// Create a SOCKS5 server
	conf := &socks5.Config{}
	server, err := socks5.New(conf)
	if err != nil {
		log.Fatalf("Error creating SOCKS5 server: %v\n", err)
	}

	// Start the SOCKS5 proxy on the specified port
	address := fmt.Sprintf("0.0.0.0:%s", *port)
	listener, err := net.Listen("tcp", address)
	if err != nil {
		log.Fatalf("Error listening on port %s: %v\n", *port, err)
	}
	defer listener.Close()

	log.Printf("SOCKS5 proxy is running on %s\n", address)
	if err := server.Serve(listener); err != nil {
		log.Fatalf("Error serving SOCKS5 proxy: %v\n", err)
	}
}
