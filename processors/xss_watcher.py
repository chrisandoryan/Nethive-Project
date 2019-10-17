import socket
import json

# Matching Algorithm. 
# Before searching for scripts in the
# HTTP request, the filter transforms the URL request (and
# any POST data) as follows:
# 1. URL decode (e.g., replace %41 with A). This step mimics the URL decoding that the server does when receiving an HTTP request (e.g., before PHP returns
# the value of $_GET["q"]).
# 2. Character set decode (e.g., replace UTF-7 code points
# with Unicode characters). This step mimics a transformation done by the HTML tokenizer.
# 3. HTML entity decode (e.g., replace &amp; with &). The
# filter applies this transformation only to some of the
# interception points. For example, inline scripts are not
# entity decoded but inline event handlers are.
# http://www.collinjackson.com/research/xssauditor.pdf

WATCHMAN_HOST = 'localhost'
WATCHMAN_PORT = 5127

def domparse(the_response, the_request, flagged_xss):
    """
        Send HTTP Response to DOM Parser to detect XSS
    """
    print(the_response)
    the_response = the_response.decode('ISO-8859-1')

    # try:
    # except Exception as e:
    #     print("[!] %s" % e)
    #     pass

    audit_package = {
        "res_body": the_response,
        "req_packet": the_request,
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((WATCHMAN_HOST, WATCHMAN_PORT))
    s.sendall(json.dumps(audit_package).encode())

    s.close()
    return

def inspect(arr_buff):
    """
        Check HTTP Request content for potential XSS payload (static analysis)
    """
    for buff in arr_buff:
        print(buff)

    return


if __name__ == "__main__":
    pass