import socket
import json

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 2345  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            try:
                parsed_data = json.loads(data)
                print(parsed_data)
            except Exception as e:
                pass
            
            if not data:
                break
            conn.sendall(data)