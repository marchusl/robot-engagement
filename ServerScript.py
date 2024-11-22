import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

message_to_send = ""
send_message = False

Debugging = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    global message_to_send, send_message, Debugging

    connected = True
    while connected:
        if send_message:
            send(conn, message_to_send)
            send_message = False
            if message_to_send == DISCONNECT_MESSAGE:
                connected = False
                Debugging = False

    conn.close()
    print(f'[CONNECTION CLOSED]')

def start():
    server.listen()
    print(f'[LISTENING] server is listening on {SERVER}')

    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def set_send_message(msg):
    global message_to_send, send_message
    message_to_send = msg
    send_message = True

start()

while Debugging:
    msg = input("Enter your message: ")
    set_send_message(msg)
