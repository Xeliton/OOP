import socket
import selectors

# to_monitor = []

selector = selectors.DefaultSelector()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)

def accept_connection(server_socket):
    print('Before .accept()')
    client_socket, addr = server_socket.accept()
    print('Connection from', addr, ' Client_socket = ', client_socket)
    # send_message(client_socket)
    # to_monitor.append(client_socket)
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    print('Before .recive()')
    request = client_socket.recv(4096)

    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        # to_monitor.remove(client_socket)
        selector.unregister(client_socket)
        client_socket.close()

    print('Outside inner while loop')


def event_loop():
    while True:
        # ready_to_read, _, _ = select(to_monitor, [], [])
        # for sock in ready_to_read:
        #     if sock is server_socket:
        #         print(sock)
        #         accept_connection(sock)
        #     else:
        #         send_message(sock)
        events = selector.select() # (key, events)
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)




if __name__ == '__main__':
    # accept_connection(server_socket)
    # to_monitor.append(server_socket)
    server()
    event_loop()
