package main

import (
	"fmt"
	"net"
	"os"

	"github.com/moovweb/gokogiri"
)

const (
	CONN_HOST = "0.0.0.0"
	CONN_PORT = "5127"
	CONN_TYPE = "tcp"
)

func main() {
	// Listen for incoming connections.
	l, err := net.Listen(CONN_TYPE, CONN_HOST+":"+CONN_PORT)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	// Close the listener when the application closes.
	defer l.Close()
	fmt.Println("Listening on " + CONN_HOST + ":" + CONN_PORT)
	for {
		// Listen for an incoming connection.
		conn, err := l.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}
		// Handle connections in a new goroutine.
		go handleRequest(conn)
	}
}

// Handles incoming requests.
func handleRequest(conn net.Conn) {
	// Make a buffer to hold incoming data.
	buf := make([]byte, 65535)
	// Read the incoming connection into the buffer.
	_, err := conn.Read(buf)
	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}

	// parse the web page
	doc, _ := gokogiri.ParseHtml(buf)

	// perform operations on the parsed page -- consult the tests for examples

	// Send a response back to person contacting us.
	conn.Write([]byte(buf))
	// Close the connection when you're done with it.
	conn.Close()

	// important -- don't forget to free the resources when you're done!
	doc.Free()
}
