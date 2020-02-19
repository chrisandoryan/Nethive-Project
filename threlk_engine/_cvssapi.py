""" A script to convert SIEM data so that CVSS may digest the data """
import datetime
def convert(result):
		def checkIfNone(ip):
			if ip == '' or ip == None:
				return "127.0.0.1"
			return ip;
		print("INPUT : {}".format(result))
		xss_data = result["EVENT_DATA"]["audit_xss"]
		sqli_data = result["EVENT_DATA"]["inspect_sqli"]
		print("sqli_data : {}".format(sqli_data))
		timestamp = str(datetime.datetime.now())
		xss_malicious = []
		sql_malicious = []
		if bool(xss_data) and "QueryParamAuditResult" in xss_data.keys():
			if bool(xss_data["QueryParamAuditResult"] != None):	
				xss_malicious = [{"_id":1335,"url":items["SinkholePath"],"ip":checkIfNone(items["ClientIP"]), "vul": "XSS","timestamp":timestamp} for items in xss_data["QueryParamAuditResult"] if items["LikelyMalicious"]==True]
		if bool(sqli_data):	
			if bool(sqli_data["inspection_result"] != None):	
				sql_malicious = [{"_id":1335,"url":sqli_data["url"],"ip":checkIfNone(sqli_data["client_ip"]), "vul": "SQLi","timestamp":timestamp} for items in sqli_data["inspection_result"] if items["classification"]=="malicious"]
		# sqli_malicious = [items for items in inspect_sqli]
		# xss_converted = [{"_id":1335,"url":items["SinkholePath"],"ip":checkIfNone(items["ClientIP"]), "vul": "XSS","timestamp":str(datetime.datetime.now())} for items in xss_malicious]
		print(xss_malicious)
		print(sql_malicious)
		return xss_malicious + sql_malicious;
