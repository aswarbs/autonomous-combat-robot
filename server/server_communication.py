import socket
import json
import io
from PIL import Image
from computer_vision.detect_rubik import ObjectDetection
from computer_vision.detect_qr import DetectQR
from decision_making.decision_maker import DecisionMaker
import numpy as np
# Set host as localhost to receive messages on this machine.
HOST = "0.0.0.0"
# Set well known port for the client to use.
PORT = 2345

detector = ObjectDetection()
decider = DecisionMaker()
qr_detector = DetectQR()

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
            received_data = receive_data(conn)
            print("received")
            image = convert_bytes_to_image(received_data)


            image_information, qr_information = recognise_image(image)

            robot_movements, state = process_information(image_information, qr_information)

            for movement in robot_movements:
                send_response(conn, movement, state)



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
    image_size_bytes = conn.recv(4)
    image_size = int.from_bytes(image_size_bytes, byteorder='big')

    # Receive the image data
    image_data = b''
    while len(image_data) < image_size:
        chunk = conn.recv(min(4096, image_size - len(image_data)))
        if not chunk:
            break
        image_data += chunk
    return image_data

def parse_data(received_data):
    try:
        # Attempt to parse the message with JSON. Agreed encoding = UTF8
        parsed_data = json.loads(received_data.decode('utf-8'))

        return parsed_data
    except:
        print("failed to parse")

   

def convert_bytes_to_image(parsed_data):
    # Retrieve the screenshot field of the JSON message

    # Create a BytesIO object to work with the image data
    image_stream = io.BytesIO(bytes(parsed_data))

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



def send_response(conn, robot_movements, state):

    success_response = {"status": "success", "movements": robot_movements, "state": state}
    conn.send(json.dumps(success_response).encode('utf-8') + b'\n')



bind_socket() 