import socket
import json
import io
from PIL import Image
import cv2
import numpy as np
import threading

class ServerCommunication():

    def __init__(self, detector, decider, qr_detector, localisation):

        print("hello")
        

        # Set host as localhost to receive messages on this machine.
        self.HOST = "127.0.0.1"
        # Set well known port for the client to use.
        self.PORT = 2345

        self.detector = detector
        self.decider = decider
        self.qr_detector = qr_detector
        self.localisation = localisation

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
            
            



    def run(self, conn, s):
        while True:
            #try:
                
                received_data = self.receive_data(conn)
                parsed_data = self.parse_data(received_data)

                image, self.movement_state, movement, rotation = self.convert_bytes_to_image(parsed_data)

                image_information, qr_information = self.recognise_image(image)


                robot_movements, state = self.process_information(image_information, qr_information)

                cv2.imshow('ROBOT POV', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if cv2.waitKey(1) == 0xFF: 
                        return  # esc to quit

                if(self.movement_state == "MANUAL"):
                    print(f"setting movement: {movement} and rotation: {rotation}")
                    self.localisation.velocity = movement
                    self.localisation.angular_velocity = rotation
                    self.send_response(conn, movement, "SUCCESS")
                    continue


                


                

                for movement in robot_movements:
                    self.localisation.velocity = movement[0]
                    self.localisation.angular_velocity = movement[1]
                    self.send_response(conn, movement, state)

                        
                """except Exception as e:
                    print("client disconnected: ", e)
                    self.localisation.velocity = 0
                    self.localisation.angular_velocity = 0
                    s.close()
                    self.bind_socket()"""

    



    def recognise_image(self,image):
        """
        Pass the image retrieved from the client to the computer vision model.
        Retrieve useful information from the image to use in the decision making.
        image: The image to be processed.
        returns: Information gathered from the image during image processing.
        """
        
        qr_information = self.qr_detector.find_qrs_and_distances(image)
        opponent_information = self.detector.run(image)
        return opponent_information, qr_information

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

        return image, state, movement, rotation

    """def save_image(image):
        # Define a filename for the saved PNG image
        filename = 'computer_vision/saved_image.png'

        # Save the image as a PNG file
        image.save(filename, 'PNG')"""



    def send_response(self, conn, robot_movements, state):

        success_response = {"status": "success", "movements": robot_movements, "state": state}
        conn.send(json.dumps(success_response).encode('utf-8') + b'\n')
