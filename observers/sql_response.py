import socket
import threading
import json
# import signal

from storage.memcache import MemCacheClient

memcache = MemCacheClient().getInstance()

bind_ip = '0.0.0.0'
bind_port = 5128

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

def keyboardInterruptHandler(signal, frame):
    server.close()

def handle_client_connection(client_socket):
    request = client_socket.recv(2048)
    try:
        request = json.loads(request.decode('utf-8'))
        client_ip = request['client_ip']
        client_port = request['client_port']
        sql_response = request['sql_response']

        memcache.update(client_ip, client_port, 'sql_response', sql_response)
        data = memcache.get(client_ip)
        print(data, "FROM RESPONSE OBSERVER")

    except Exception as e:
        print("[!] %s" % e)
    

def run():
    print('[SQL_Response_Observer] Listening on {}:{}'.format(bind_ip, bind_port))

    # --- Set signal handlers
    # signal.signal(signal.SIGINT, keyboardInterruptHandler)

    while True:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

if __name__ == "__main__":
    run()