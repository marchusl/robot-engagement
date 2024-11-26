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
service_in_progress = False

current_head_position = ""

Debugging = True

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
            listen_for_completions(conn)
            if message_to_send == DISCONNECT_MESSAGE:
                connected = False
                Debugging = False

    conn.close()
    print(f'[CONNECTION CLOSED]')

def listen_for_completions(conn):
    print(f'Listening for confirmation:')
    global service_in_progress

    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        print(f'Confirmation received from client: {msg}')
        service_in_progress = False
        # print(service_in_progress)

        #confirm_completion = msg

        #return confirm_completion

def start_socket_streaming():
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

def set_send_message(msg):      # Use this for Gestures (Maybe make a separate function for head rotations wherein the global currentGlobalHeadOrientation is set, so it is only updated when actually rotating/orienting the head of the robot)
    global message_to_send, send_message, service_in_progress, current_head_position
    message_to_send = msg
    send_message = True
    service_in_progress = True
    # print(service_in_progress)

    # Check message to update global current head position
    if "[GESTURE]" in msg:
        split_message = msg.split("-")
        if len(split_message) == 3:
            new_position = split_message[2]
            current_head_position = new_position
        elif len(split_message) <= 2:
            new_position = "neutral"
            current_head_position = new_position
        else:
            print(f"Could not set current head position: {msg}")

        print(f"Current Head Position: {current_head_position}")

if __name__ == "__main__":
    start_socket_streaming()

    while Debugging:
        msg = input("Enter your message: ")
        set_send_message(msg)
