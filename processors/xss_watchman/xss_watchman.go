package main

import (
	"fmt"
	"net"
	"os"
	"strings"
	"encoding/json"

	"github.com/jbowtie/gokogiri"
)

const (
	connHost = "localhost"
	connPort = "5127"
	connType = "tcp"
)

type AuditPackage struct {
	ItsResponse string `json:"response_body"`
	ItsRequest string `json:"request_packet"`
}

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

func compareWithRequest(afterParse string, originalRequest string) bool {
	// Could also perform data transformation here (to prevent obfuscation)
	fmt.Println(afterParse, originalRequest)
	return strings.Contains(originalRequest, afterParse)
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

	var audit AuditPackage
	json.Unmarshal([]byte(buf), &audit)

	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}

	doc, err := gokogiri.ParseHtml([]byte(audit.ItsResponse))

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
				fmt.Println(i, scriptInnerHTML)
				if compareWithRequest(scriptInnerHTML, audit.ItsRequest) {
					fmt.Println("DETECTED1!")
				}
			}

			// --- Check if src attribute appears in here and contains the user input
			scriptSrcAttr := ist.Attr("src")
			if scriptSrcAttr != "" {
				fmt.Println(i, scriptSrcAttr)
				if compareWithRequest(scriptSrcAttr, audit.ItsRequest) {
					fmt.Println("DETECTED2!")
				}
			}
		}

		// --- Check appearance of JS url or event-handler
		for j, attr := range s.Attributes() {
			if stringInSlice(attr.String(), extContentAttrs) {
				fmt.Print(j, attr)
			}
		}
	}

	conn.Write([]byte("doc"))
	conn.Close()

	doc.Free()
}

// echo -n "<html><body onload=javascript:alert(1)><div><h1></div>" | nc localhost 5127
// nc localhost 5127 < example.html
