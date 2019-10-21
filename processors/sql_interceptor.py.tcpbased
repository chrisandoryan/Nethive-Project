import socket
import threading
import json
import signal

bind_ip = '0.0.0.0'
bind_port = 5128

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

def keyboardInterruptHandler(signal, frame):
    server.close()

def handle_client_connection(client_socket):
    request = client_socket.recv(2048)
    print(request)
    try:
        request = json.loads(request.decode('utf-8'))
    except Exception as e:
        print("[!] %s" % e)
    if request['mysql']['num_rows'] > 0:
        query = request['query']
        result = request['response']
        print("===============")
        print(query)
        for row in result.splitlines()[1:]:
            print(row)
        print("===============")
    else:
        print("Skipping because of zero rows return")
    client_socket.close()

def main():
    # --- Set signal handlers
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    while True:
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)
        )
        client_handler.start()

if __name__ == "__main__":
    print('[SQL_Interceptor] Listening on {}:{}'.format(bind_ip, bind_port))
    main()