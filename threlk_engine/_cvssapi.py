""" A script to convert SIEM data so that CVSS may digest the data """

import datetime
def convert(result):
		print("result {}".format(result))
		xss_data = result["EVENT_DATA"]["audit_xss"]
		sqli_data = result["EVENT_DATA"]["inspect_sqli"]
		print("XSS {}".format(xss_data))
		print("SQL {}".format(sqli_data))
		""" check for True result """
		xss_malicious = []
		sqli_malicious = []
		if xss_data != None:
			print("Scan XSS")
			if xss_data.get("QueryParamAuditResult") and xss_data["QueryParamAuditResult"]!=None:
				xss_malicious = [items for items in xss_data["QueryParamAuditResult"] if items["LikelyMalicious"]==True]
		if sqli_data != None:
			print("Scan SQL")
			sqli_malicious = [items for items in sqli_data["inspection_result"] if items["classification"] == "malicious"]
		print("TEST")
		print(xss_malicious)
		print(sqli_malicious)
		# sqli_malicious = [items for items in inspect_sqli]
		def checkIfNone(ip):
			if ip == None:
				return "127.0.0.1"
			return ip;
		converted = []
		if len(xss_malicious) > 0:
			converted = [{"_id":1335,"url":items["SinkholePath"],"ip":checkIfNone(items["ClientIP"]), "vul": "XSS","timestamp":str(datetime.datetime.now())} for items in xss_malicious]
		if len(sqli_malicious) > 0:
			converted = [{"_id":1335,"url":sqli_data["url"],"ip":checkIfNone(sqli_data["client_ip"]), "vul": "SQLi","timestamp":str(datetime.datetime.now())}]

		return converted;
