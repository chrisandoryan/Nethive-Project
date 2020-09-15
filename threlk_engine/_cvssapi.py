""" A script to convert SIEM data so that CVSS may digest the data """

import datetime

def convert(result):
		if not result["EVENT_TYPE"] is "HTTP_MONITOR":
			return []

		id = result["EVENT_DATA"]["arrived_at"]
		xss_data = result["EVENT_DATA"]["audit_xss"]
		sqli_data = result["EVENT_DATA"]["inspect_sqli"]
		""" check for True result """
		xss_malicious = []
		sqli_malicious = []
		if xss_data != None and xss_data:
			if xss_data.get("QueryParamAuditResult") and xss_data["QueryParamAuditResult"]!=None:
				xss_malicious = [items for items in xss_data["QueryParamAuditResult"] if items["LikelyMalicious"]==True]
		if sqli_data != None and sqli_data:
			print("[SQLi Data]", sqli_data)
			sqli_malicious = [items for items in sqli_data["inspection_result"] if items["classification"] == "malicious"]

		# sqli_malicious = [items for items in inspect_sqli]
		def checkIfNone(ip):
			if ip == None:
				return "127.0.0.1"
			return ip;
		converted = []
		if len(xss_malicious) > 0:
			converted = [{"_id":id,"url":items["SinkholePath"],"ip":checkIfNone(items["ClientIP"]), "payload":items["Payload"], "vul": "XSS","timestamp":str(datetime.datetime.now())} for items in xss_malicious]
		if len(sqli_malicious) > 0:
			converted = [{"_id":id,"url":sqli_data["url"],"ip":checkIfNone(sqli_data["client_ip"]), "payload": ", ".join([x["payload"] for x in sqli_malicious]), "vul": "SQLi", "timestamp":str(datetime.datetime.now())}]
		# print(converted)
		return converted
