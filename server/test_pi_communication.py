import socket
HOST = '0.0.0.0'
PORT = 9999
from picamera2 import Picamera2
import serial  
import json

ser = None




def bind_socket():

    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280,720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

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
            image= picam2.capture_array()
            send_response(conn)

def send_response(conn):
    success_response = b"hello from server"
    conn.send(success_response)

def send_response_arduino(movement, state):
    response = {"movement": movement[0], "rotation": movement[1], "state": state}
    ser.write(json.dumps(response).encode('utf-8') + b'\n')

bind_socket()