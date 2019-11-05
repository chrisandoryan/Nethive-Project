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
	connHost = "127.0.0.1"
	connPort = "5127"
	connType = "tcp"
)

const (
	constNotLikelyInjection               = 0
	constInjectionFromQueryParam          = 1
	constInjectionLocationFromQueryParam  = "QUERY_PARAM"
	constInjectionFromRequestBody         = 2
	constInjectionLocationFromRequestBody = "REQUEST_BODY"
	constInjectionFromSQLResponse         = 3
	constInjectionLocationFromSQLResponse = "SQL_RESPONSE"
)

const (
	constMethodNameCheckInlineScript        = "CHECK_INLINE_SCRIPT"
	constMethodNameCheckDangerousAttributes = "CHECK_DANGEROUS_ATTRS"
	constMethodNameCheckExternalContent     = "CHECK_EXT_CONTENT"
)

const (
	storeNonMaliciousAuditReportAsWell = true //change to true to report non-malicious audit report as well (more processing, more storage used)
)

// AuditResultPackage contains ...
type AuditResultPackage struct {
	SQLResponseAuditResult []AuditReport
	QueryParamAuditResult  []AuditReport
	RequestBodyAuditResult []AuditReport
}

// AuditReport contains ...
type AuditReport struct {
	LikelyMalicious      bool // is the result indicates malicious activity?
	ClientIP             string
	ClientPort           string
	Payload              string
	PayloadLocation      string // where is the payload located? URL? Body? SQL Response?
	SinkholePath         string // which source code file is affected/injected?
	TriggeredCheckMethod string // which method detected the payload as malicious?
	Time                 string // time the auditing process is finished
}

// RequestPacket contains ...
type RequestPacket struct {
	URL         string              `json:"url"`
	Body        string              `json:"body"`
	SQLResponse []map[string]string `json:"sql_response"`
	ClientIP    string              `json:"client_ip"`
	ClientPort  string              `json:"client_port"`
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
	fmt.Println("Comparing " + strings.ToLower(aString) + " with " + strings.ToLower(aSubstring))
	return strings.Contains(strings.ToLower(aString), strings.ToLower(aSubstring))
}

func hasPrefixIgnoreCase(aString string, aPrefix string) bool {
	return strings.HasPrefix(strings.ToLower(aString), strings.ToLower(aPrefix))
}

func constructAuditResultRecapitulation(checkCalledFrom string, inspectedElement string, originalRequest RequestPacket, reqComparisonResults []int, recapAuditResult *AuditResultPackage) {

	for _, reqComparisonValue := range reqComparisonResults {
		switch reqComparisonValue {
		case constNotLikelyInjection:
			if storeNonMaliciousAuditReportAsWell {
				auditReport := AuditReport{
					LikelyMalicious: false,
					Payload:         inspectedElement,
					ClientIP:        originalRequest.ClientIP,
					ClientPort:      originalRequest.ClientPort,
				}
				fmt.Println(auditReport)
				// recapAuditResult.QueryParamAuditResult = append(recapAuditResult.QueryParamAuditResult, auditReport)
			}
			break
		case constInjectionFromQueryParam:
			auditReport := AuditReport{
				LikelyMalicious:      true,
				Payload:              inspectedElement,
				PayloadLocation:      constInjectionLocationFromQueryParam,
				TriggeredCheckMethod: checkCalledFrom,
				ClientIP:             originalRequest.ClientIP,
				ClientPort:           originalRequest.ClientPort,
			}
			// fmt.Println(auditReport)
			recapAuditResult.QueryParamAuditResult = append(recapAuditResult.QueryParamAuditResult, auditReport)
			break
		case constInjectionFromRequestBody:
			auditReport := AuditReport{
				LikelyMalicious:      true,
				Payload:              inspectedElement,
				PayloadLocation:      constInjectionLocationFromRequestBody,
				TriggeredCheckMethod: checkCalledFrom,
				ClientIP:             originalRequest.ClientIP,
				ClientPort:           originalRequest.ClientPort,
			}
			// fmt.Println(auditReport)
			recapAuditResult.RequestBodyAuditResult = append(recapAuditResult.RequestBodyAuditResult, auditReport)
			break
		case constInjectionFromSQLResponse:
			auditReport := AuditReport{
				LikelyMalicious:      true,
				Payload:              inspectedElement,
				PayloadLocation:      constInjectionLocationFromSQLResponse,
				TriggeredCheckMethod: checkCalledFrom,
				ClientIP:             originalRequest.ClientIP,
				ClientPort:           originalRequest.ClientPort,
			}
			// fmt.Println(auditReport)
			recapAuditResult.SQLResponseAuditResult = append(recapAuditResult.SQLResponseAuditResult, auditReport)
			break
		}
	}
}

func compareWithRequest(afterParse string, originalRequest RequestPacket) []int {
	// FIXME: perform data transformation here (to prevent obfuscation)
	// fmt.Println(afterParse, originalRequest.URL)
	// fmt.Println(afterParse, originalRequest.Body)

	fromQueryParam, fromRequestBody, fromSQLResponse := 0, 0, 0
	// fmt.Println(originalRequest.SQLResponse)
	for _, response := range originalRequest.SQLResponse {
		for _, payload := range response {
			// fmt.Println("key:", key, "payload:", payload)
			if containsIgnoreCase(payload, afterParse) {
				fromSQLResponse = constInjectionFromSQLResponse
				break
			}
		}
		if fromSQLResponse > 0 {
			break
		}
	}

	if containsIgnoreCase(originalRequest.URL, afterParse) {
		fromQueryParam = constInjectionFromQueryParam
	}

	if containsIgnoreCase(originalRequest.Body, afterParse) {
		fromRequestBody = constInjectionFromRequestBody
	}

	return []int{fromQueryParam, fromRequestBody, fromSQLResponse}
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
	var recapAuditResult AuditResultPackage

	err := d.Decode(&audit)

	// fmt.Println(audit)

	// fmt.Println(audit.ItsRequest, err)
	// fmt.Println(audit.ItsResponse, err)

	if err != nil {
		fmt.Println("Error reading:", err.Error())
		return
	}

	if audit.ItsResponse == "" {
		fmt.Println("Response is empty")
		// return
	}

	doc, err := gokogiri.ParseHtml([]byte(audit.ItsResponse))

	if err != nil {
		fmt.Println("Parsing has error:", err)
		// return
	}

	inlineScriptTags, _ := doc.Root().Search("//script")
	for _, scriptTag := range inlineScriptTags {
		// --- Check Inline Script Tags
		// the Auditor checks whether the content of the script is contained within the request
		scriptInnerHTML := scriptTag.InnerHtml()
		if scriptInnerHTML != "" {
			// fmt.Println(i, scriptInnerHTML)
			var firstHundredCharacters = getPossiblyDangerousHundredCharacters(scriptInnerHTML)

			constructAuditResultRecapitulation(constMethodNameCheckInlineScript, firstHundredCharacters, audit.ItsRequest, compareWithRequest(firstHundredCharacters, audit.ItsRequest), &recapAuditResult)

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
				attributeValue := attrValue.String()

				constructAuditResultRecapitulation(constMethodNameCheckDangerousAttributes, attributeValue, audit.ItsRequest, compareWithRequest(attributeValue, audit.ItsRequest), &recapAuditResult)
			}
		}
	}

	// --- Check External Content (Specific Tags)
	for _, tagName := range extContentTagList {
		targetTags, _ := doc.Root().Search(".//" + tagName)
		for _, tag := range targetTags {
			for attr, attrValue := range tag.Attributes() {
				if stringInSlice(attr, extContentAttrList) {
					attributeValue := attrValue.String()

					constructAuditResultRecapitulation(constMethodNameCheckExternalContent, attributeValue, audit.ItsRequest, compareWithRequest(attributeValue, audit.ItsRequest), &recapAuditResult)

				}
			}
		}
	}

	foo, err := json.Marshal(recapAuditResult)
	if err != nil {
		fmt.Println(err)
		return
	}

	conn.Write([]byte(foo))
	conn.Close()

	doc.Free()
}

// echo -n "<html><body onload=javascript:alert(1)><div><h1></div>" | nc localhost 5127
// nc localhost 5127 < example.html
