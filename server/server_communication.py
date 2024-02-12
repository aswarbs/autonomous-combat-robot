import socket
import json
import io
from PIL import Image
from computer_vision.detect_rubik import ObjectDetection
from computer_vision.detect_qr import DetectQR
from decision_making.decision_maker import DecisionMaker
import numpy as np
from picamera2 import Picamera2
import serial   

# Set host as localhost to receive messages on this machine.
HOST = "127.0.0.1"
# Set well known port for the client to use.
PORT = 2345

detector = ObjectDetection()
decider = DecisionMaker()
qr_detector = DetectQR()

def bind_socket():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1280,720)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:

        pass
        """image= picam2.capture_array()


        image_information, qr_information = recognise_image(image)

        robot_movements, state = process_information(image_information, qr_information)

        for movement in robot_movements:
            send_response(ser, movement)

        line = ser.readline().decode('utf-8').rstrip()
        print(line)"""



def recognise_image(image):
    """
    Pass the image retrieved from the client to the computer vision model.
    Retrieve useful information from the image to use in the decision making.
    image: The image to be processed.
    returns: Information gathered from the image during image processing.
    """
    opponent_information = detector.run(image)
    qr_information = qr_detector.find_qrs_and_distances(image)
    return opponent_information, qr_information

def process_information(image_information, qr_information):
    """
    Pass information gathered about an image to the decision making model.
    image_information: The information about the image.
    """
    
    robot_movements, state = decider.run(image_information, qr_information)
    return robot_movements, state



        
def receive_data(conn):
    # Initialize an empty byte string to accumulate data
    received_data = b""  

    while True:
        # Receive 1024 bytes of data
        data = conn.recv(1024)

        # Append the newly received data to the current item of data being collected
        received_data += data  

        # If the message delimiter is in the message, the end of the message has been found
        if b'\n' in data:
            break
    return received_data

def parse_data(received_data):
    try:
        # Attempt to parse the message with JSON. Agreed encoding = UTF8
        parsed_data = json.loads(received_data.decode('utf-8'))
        return parsed_data
    except:
        print("failed to parse")

   

def convert_bytes_to_image(parsed_data):
    # Retrieve the screenshot field of the JSON message
    image_data_byte_array = parsed_data['screenshotPNG']

    # Create a BytesIO object to work with the image data
    image_stream = io.BytesIO(bytes(image_data_byte_array))

    # Open the image using PIL (Pillow)
    image = Image.open(image_stream)

    # PIL images into NumPy arrays
    image = np.asarray(image)

    return image

"""def save_image(image):
    # Define a filename for the saved PNG image
    filename = 'computer_vision/saved_image.png'

    # Save the image as a PNG file
    image.save(filename, 'PNG')"""



def send_response(ser, robot_movements):

    response = {"movement": robot_movements[0], "rotation": robot_movements[1]}
    ser.write(json.dumps(response).encode('utf-8') + b'\n')
    



bind_socket() 