import socket
import json
import io
from PIL import Image
import cv2
import numpy as np
import math
from datetime import datetime

class ServerCommunication():

    def __init__(self, detector, decider, qr_detector, localisation):

        # Set host as localhost to receive messages on this machine.
        self.HOST = "127.0.0.1"
        # Set well known port for the client to use.
        self.PORT = 2345

        """self.detector = detector
        self.decider = decider"""
        self.qr_detector = qr_detector
        #self.localisation = localisation

    def bind_socket(self):

        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # Bind the socket to the host and port
            s.bind((self.HOST, self.PORT))

            print("listening")

            # Listen for incoming messages on the socket
            s.listen()

            print("connected")

            # Accept the message on the socket, addr = the client host and port, conn = the connection.
            conn, addr = s.accept()

            
            self.run(conn, s)
            
            
    def draw_arrow(self, orientation, bounding_box_width, bounding_box_height, image, center_x, center_y):
        orientation = (orientation * -1) + 90 # convert to angle used in function (0 is right)

        # Calculate the endpoint of the arrow
        arrow_length = 50  # You can adjust the arrow length as needed

        center_x = bounding_box_width / 2
        center_y = bounding_box_height / 2


        arrow_endpoint_x = int(center_x + arrow_length * math.cos(math.radians(orientation)))
        arrow_endpoint_y = int(center_y + arrow_length * math.sin(math.radians(orientation)))

        cv2.arrowedLine(image, ((int)(center_x), (int)(center_y)), (arrow_endpoint_x, arrow_endpoint_y), (0, 0, 255), 2)


    def timestamp_to_milliseconds(self, timestamp):

        timestamp = str(timestamp)
        hour, minute, secs_and_millis = timestamp.split(":")

        if("." not in secs_and_millis):
            second = secs_and_millis
            millisecond = 0
        else:
            second, millisecond = secs_and_millis.split(".")
        seconds = int(hour) * 60 * 60 + int(minute) * 60 + int(second)
        seconds += float(millisecond) / 1000
        milliseconds = seconds * 1000

        return milliseconds / 1000000


    def run(self, conn, s):
        while True:
            #try:
                
                received_data = self.receive_data(conn)
                parsed_data = self.parse_data(received_data)

                image, self.movement_state, movement, rotation, time = self.convert_bytes_to_image(parsed_data)

                format = '%H:%M:%S:%f'
                current_time = datetime.utcnow().strftime(format)[:-3]

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                self.recognise_image(image)

                """image_information, qr_information = self.recognise_image(image)

                map(lambda d: self.draw_image_information(d, image), image_information if image_information is not None else [])

                robot_movements, state = self.process_information(image_information, qr_information)"""

                difference = datetime.strptime(current_time, format) - datetime.strptime(time, format)
                milliseconds = self.timestamp_to_milliseconds(difference)



                cv2.imshow('ROBOT POV', image)
                if cv2.waitKey(1) == 0xFF: 
                        return  # esc to quit

                if(self.movement_state == "MANUAL"):
                    self.localisation.set_velocity(movement)
                    self.localisation.set_angular_velocity(rotation)
                    self.localisation.time_difference = milliseconds
                    self.send_response(conn, movement, "SUCCESS")
                    continue



                """for movement in robot_movements:
                    self.localisation.velocity = movement[0]
                    self.localisation.angular_velocity = movement[1]
                    self.localisation.time_difference = milliseconds
                    self.send_response(conn, movement, state)"""

            

    
    def draw_image_information(self, image_information, image):
        (x1, y1, x2, y2) = image_information["position"]
        orientation = image_information["orientation"]
        bounding_box_area = image_information["bounding_box_area"]

        # Calculate the width and height of the bounding box
        width = x2 - x1
        height = y2 - y1

        center_x = (x1 + y2) / 2
        center_y = (y1 + y2) / 2

        
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), 1)
        self.draw_arrow(orientation, width, height, image, center_x, center_y)




    def recognise_image(self,image):
        """
        Pass the image retrieved from the client to the computer vision model.
        Retrieve useful information from the image to use in the decision making.
        image: The image to be processed.
        returns: Information gathered from the image during image processing.
        """
        
        qr_information = self.qr_detector.find_qrs_and_distances(image)
        #opponent_information = self.detector.run(image)
        #return opponent_information, qr_information

    def process_information(self, image_information, qr_information):
        """
        Pass information gathered about an image to the decision making model.
        image_information: The information about the image.
        """
        
        robot_movements, state = self.decider.run(image_information, qr_information)

        return robot_movements, state



            
    def receive_data(self, conn):
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

    def parse_data(self, received_data):
        try:
            # Attempt to parse the message with JSON. Agreed encoding = UTF8
            parsed_data = json.loads(received_data.decode('utf-8'))
            return parsed_data
        except:
            print("failed to parse")

    

    def convert_bytes_to_image(self, parsed_data):
        # Retrieve the screenshot field of the JSON message
        image_data_byte_array = parsed_data['screenshotPNG']

        # Create a BytesIO object to work with the image data
        image_stream = io.BytesIO(bytes(image_data_byte_array))

        # Open the image using PIL (Pillow)
        image = Image.open(image_stream)

        # PIL images into NumPy arrays
        image = np.array(image)

        state = parsed_data['movementState']

        movement = parsed_data['movement']
        rotation = parsed_data['rotation']

        time = parsed_data["time"]

        

        return image, state, movement, rotation, time

    """def save_image(image):
        # Define a filename for the saved PNG image
        filename = 'computer_vision/saved_image.png'

        # Save the image as a PNG file
        image.save(filename, 'PNG')"""



    def send_response(self, conn, robot_movements, state):

        success_response = {"status": "success", "movements": robot_movements, "state": state}
        conn.send(json.dumps(success_response).encode('utf-8') + b'\n')
