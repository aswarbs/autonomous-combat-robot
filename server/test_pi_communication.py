import socket
HOST = '0.0.0.0'
PORT = 9999


def bind_socket():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Bind the socket to the host and port
        s.bind((HOST, PORT))

        print("listening")

        # Listen for incoming messages on the socket
        s.listen()

        # Accept the message on the socket, addr = the client host and port, conn = the connection.
        conn, addr = s.accept()

        print("connected")

        while True:
            send_response(conn)

def send_response(conn):
    success_response = b"hello from server"
    conn.send(success_response)

bind_socket()