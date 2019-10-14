package main

import (
	"fmt"
	"net"
	"os"

	"github.com/jbowtie/gokogiri"
)

const (
	connHost = "0.0.0.0"
	connPort = "5127"
	connType = "tcp"
)

var safeJavaScriptURL = []string{"javascript:void(0)"}
var extContentAttrs = []string{"src"}

func main() {
	// Listen for incoming connections.
	l, err := net.Listen(connType, connHost+":"+connPort)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	// Close the listener when the application closes.
	defer l.Close()
	fmt.Println("Listening on " + connHost + ":" + connPort)

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

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func handleRequest(conn net.Conn) {
	buf := make([]byte, 65535)
	_, err := conn.Read(buf)
	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}

	doc, err := gokogiri.ParseHtml([]byte(buf))

	if err != nil {
		fmt.Println("Parsing has error:", err)
		return
	}

	rootParse, _ := doc.Root().Search(".//*")
	for _, s := range rootParse {
		// --- Find <script> tags
		inlineScriptTags, _ := s.Search("//script")
		for i, ist := range inlineScriptTags {
			// --- Check if the user input appears in here
			scriptInnerHTML := ist.InnerHtml()
			if scriptInnerHTML != "" {
				fmt.Println(i, ist.InnerHtml())
			}

			// --- Check if url attributes appears in here (src, attr, data, etc)
			for j, attr := range ist.Attributes() {
				if stringInSlice(attr.String(), extContentAttrs) {
					fmt.Print(j, attr)
				}
			}
		}

		// --- Check appearance of JS url or event-handler

	}

	conn.Write([]byte("doc"))
	conn.Close()

	doc.Free()
}

// echo -n "<html><body onload=javascript:alert(1)><div><h1></div>" | nc localhost 5127
// nc localhost 5127 < example.html
