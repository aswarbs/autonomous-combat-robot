import socket
import json
import io
from PIL import Image
from computer_vision.detect_rubik import ObjectDetection
from computer_vision.detect_qr import DetectQR
from decision_making.decision_maker import DecisionMaker
import numpy as np
import keyboard
import base64
# Set host as localhost to receive messages on this machine.
HOST = "192.168.1.121"
# Set well known port for the client to use.
PORT = 9999
import cv2

detector = ObjectDetection()
decider = DecisionMaker()
qr_detector = DetectQR()

# handle autonomous / manual here

movement_mode = "MANUAL"
manual_movements = [0,0]

def bind_socket():


    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Bind the socket to the host and port
        s.bind((HOST, PORT))

        print("listening")

        # Listen for incoming messages on the socket
        s.listen()

        print("connected")

        # Accept the message on the socket, addr = the client host and port, conn = the connection.
        conn, addr = s.accept()


        while True:

            received_data = receive_data(conn)
            parsed_data = parse_data(received_data)

            image = convert_bytes_to_image(parsed_data)


            if movement_mode == "AUTO":
                image_information, qr_information = recognise_image(image)
                robot_movements, state = process_information(image_information, qr_information)

            elif movement_mode == "MANUAL":

                if keyboard.is_pressed("w"):
                    print(f"move forward")

                if keyboard.is_pressed("a"):
                    print(f"turn left")

                if keyboard.is_pressed("s"):
                    print(f"move back")

                if keyboard.is_pressed("d"):
                    print(f"turn right")

                if keyboard.is_pressed(" "):
                    print(f"stop")

                if keyboard.is_pressed("q"):
                    print(f"change modes")


                robot_movements = manual_movements

                

            for movement in robot_movements:
                
                send_response(conn, movement, movement_mode)

            



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
    # Retrieve the base64-encoded image data
    base64_image_data = parsed_data['screenshotPNG']

    # Decode the base64 string to bytes
    image_data_bytes = base64.b64decode(base64_image_data)

    # Create a BytesIO object from the decoded bytes
    image_stream = io.BytesIO(image_data_bytes)

    # Open the image using PIL (Pillow)
    image = Image.open(image_stream)

    # Convert the PIL Image to a NumPy array
    image_array = np.array(image)

    # Convert RGB to BGR (this step is necessary only if your image is in color)
    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

    cv2.imshow("", image_array)
    cv2.waitKey(0)

    # Convert PIL images into NumPy arrays if needed
    # If you just need to display or save the image, you can use image.show() or image.save() directly
    image_np = np.asarray(image)

    return image_np

"""def save_image(image):
    # Define a filename for the saved PNG image
    filename = 'computer_vision/saved_image.png'

    # Save the image as a PNG file
    image.save(filename, 'PNG')"""

def send_response(conn, robot_movements, state):

        success_response = {"status": "success", "movements": robot_movements, "state": state}
        conn.send(json.dumps(success_response).encode('utf-8') + b'\n')
    



bind_socket() 