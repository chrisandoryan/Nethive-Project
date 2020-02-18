""" A script to convert SIEM data so that CVSS may digest the data """

import datetime
def convert(result):
		print("result {}".format(result))
		xss_data = result["EVENT_DATA"]["audit_xss"]
		sqli_data = result["EVENT_DATA"]["inspect_sqli"]
		""" check for True result """
		xss_malicious = [items for items in xss_data["QueryParamAuditResult"] if items["LikelyMalicious"]==True]
		print(xss_malicious)

		# sqli_malicious = [items for items in inspect_sqli]
		def checkIfNone(ip):
			if ip == '':
				return "127.0.0.1"
			return ip;
		xss_converted = [{"_id":1335,"url":items["SinkholePath"],"ip":checkIfNone(items["ClientIP"]), "vul": "XSS","timestamp":str(datetime.datetime.now())} for items in xss_malicious]
		return xss_converted;
