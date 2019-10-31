package main

import (
	"encoding/json"
	"fmt"
	"net"
	"os"
	"strings"

	"github.com/jbowtie/gokogiri"
)

const (
	connHost = "localhost"
	connPort = "5127"
	connType = "tcp"
)

type SQLResponse struct {
}

// RequestPacket contains
type RequestPacket struct {
	URL    string      `json:"url"`
	Body   string      `json:"body"`
	FromDb SQLResponse `json:"sql_response"`
}

// AuditPackage contains parsed json data from xss_watcher
type AuditPackage struct {
	ItsResponse string        `json:"res_body"`
	ItsRequest  RequestPacket `json:"req_packet"`
}

var safeJavaScriptURL = []string{"javascript:void(0)"}

// Might not use this anymore since there are so many on* attributes
var eventHandlerAttrList = []string{"onload", "onerror", "onclick", "oncut", "onunload", "onfocus", "onblur", "onpointerover", "onpointerdown"}

var extContentTagList = []string{"script", "object", "param", "embed", "applet", "iframe", "meta", "base", "form", "input", "button"}
var extContentAttrList = []string{"src", "code", "data", "content", "href"}

func main() {
	// Listen for incoming connections.
	l, err := net.Listen(connType, connHost+":"+connPort)
	if err != nil {
		fmt.Println("Error listening:", err.Error())
		os.Exit(1)
	}
	// Close the listener when the application closes.
	defer l.Close()
	fmt.Println("[XSS_Auditor] Listening on " + connHost + ":" + connPort)

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

func tagHasEventHandler(attrName string) bool {
	return hasPrefixIgnoreCase(attrName, "on")
}

func containsIgnoreCase(aString, aSubstring string) bool {
	return strings.Contains(strings.ToLower(aString), strings.ToLower(aSubstring))
}

func hasPrefixIgnoreCase(aString string, aPrefix string) bool {
	return strings.HasPrefix(strings.ToLower(aString), strings.ToLower(aPrefix))
}

func compareWithRequest(afterParse string, originalRequest RequestPacket) bool {
	// ADDME: perform data transformation here (to prevent obfuscation)
	// fmt.Println(afterParse, originalRequest.URL)
	// fmt.Println(afterParse, originalRequest.Body)
	return containsIgnoreCase(originalRequest.URL, afterParse) || containsIgnoreCase(originalRequest.Body, afterParse) || containsIgnoreCase(originalRequest.SQLResponse, afterParse)
}

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func getPossiblyDangerousHundredCharacters(aString string) string {
	if commentIndex := strings.Index(aString, "//"); commentIndex >= 0 {
		return aString[:commentIndex]
	} else if len(aString) >= 100 {
		return aString[:100]
	}
	return aString
}

func isJavascriptURL(a string) bool {
	return hasPrefixIgnoreCase(a, "javascript:")
}

func handleRequest(conn net.Conn) {
	// buf := make([]byte, 65535)
	// _, err := conn.Read(buf)

	d := json.NewDecoder(conn)

	var audit AuditPackage

	err := d.Decode(&audit)
	// fmt.Println(audit.ItsRequest, err)
	// fmt.Println(audit.ItsResponse, err)

	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}

	doc, err := gokogiri.ParseHtml([]byte(audit.ItsResponse))

	if err != nil {
		fmt.Println("Parsing has error:", err)
		return
	}

	inlineScriptTags, _ := doc.Root().Search("//script")
	for _, scriptTag := range inlineScriptTags {
		// --- Check Inline Script Tags
		// the Auditor checks whether the content of the script is contained within the request
		scriptInnerHTML := scriptTag.InnerHtml()
		if scriptInnerHTML != "" {
			// fmt.Println(i, scriptInnerHTML)
			var hundredCharacters = getPossiblyDangerousHundredCharacters(scriptInnerHTML)
			if compareWithRequest(hundredCharacters, audit.ItsRequest) {
				fmt.Println(hundredCharacters, scriptTag)
				fmt.Println("DETECTED1!")
			}
		}
	}

	rootParse, _ := doc.Root().Search(".//*")
	for _, tag := range rootParse {
		// --- Check Dangerous HTML Attributes
		for attr, attrValue := range tag.Attributes() {
			// 1. checks whether the attribute contains a JavaScript URL
			// 2. whether the attribute is an event handler
			// 3. and if the complete attribute (content?) is contained in the request
			if tagHasEventHandler(attr) || isJavascriptURL(attrValue.String()) {
				if compareWithRequest(attrValue.String(), audit.ItsRequest) {
					fmt.Println(attr, attrValue)
					fmt.Println("DETECTED2!")
				}
			}
		}
	}

	// --- Check External Content (Specific Tags)
	for _, tagName := range extContentTagList {
		targetTags, _ := doc.Root().Search(".//" + tagName)
		for _, tag := range targetTags {
			for attr, attrValue := range tag.Attributes() {
				if stringInSlice(attr, extContentAttrList) {
					if compareWithRequest(attrValue.String(), audit.ItsRequest) {
						fmt.Println(attr, attrValue)
						fmt.Println("DETECTED3!")
					}
				}
			}
		}
	}

	conn.Write([]byte("doc"))
	conn.Close()

	doc.Free()
}

// echo -n "<html><body onload=javascript:alert(1)><div><h1></div>" | nc localhost 5127
// nc localhost 5127 < example.html
