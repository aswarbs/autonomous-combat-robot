import socket
HOST = '192.168.1.121'
PORT = 9999
from picamera2 import Picamera2
import serial  
import json
from PIL import Image
import base64

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

        s.connect((HOST, PORT))

        while True:
            image= picam2.capture_array()
            im = Image.fromarray(image)
            im.save('file.png')
            send_response(s)

def send_response(s):
    with open("file.png", 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    json_data = json.dumps({"screenshotPNG": encoded_string, "movementState": "ERROR", "movement": 0, "rotation": 0, "time": 0}) + "\n"
    # Encode your JSON data to bytes, then concatenate b"\n" to signify the end of the message
    final_data = json_data.encode('utf-8')
    
    # Send the final data through the socket
    s.send(final_data)

def send_response_arduino(movement, state):
    response = {"movement": movement[0], "rotation": movement[1], "state": state}
    ser.write(json.dumps(response).encode('utf-8') + b'\n')

bind_socket()