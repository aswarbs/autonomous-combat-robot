import socket
import json
import io
from PIL import Image
import cv2
import numpy as np
import math
from datetime import datetime



class ServerCommunication():

    def run_on_vid(self):
        vid = r"c:\Users\amber\Videos\demo\phonevid.mp4"
        # Open the video file
        cap = cv2.VideoCapture(vid)
        images = []

        # Check if the video was opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")
        else:
            # Read and display frame by frame
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Reached the end of the video or error in reading the video.")
                    break
                frame = self.run_on_frame(frame)
                images.append(frame)


                
        video_name = 'real1.mp4'
        frame_rate = 24  # frames per second

        # Determine the width and height from the first image
        height, width, layers = images[0].shape

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec used to create the video
        video = cv2.VideoWriter(video_name, fourcc, frame_rate, (width, height))

        # Create video
        for img in images:
            video.write(img)  # Add each image to the video

        video.release()
        cv2.destroyAllWindows()

    def run_on_frame(self, image):
            
            #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            image_information, qr_information = self.recognise_image(image)

            if image_information is not None and len(image_information) > 0:
                self.draw_image_information(image_information[0], image)

            robot_movements, state = self.process_information(image_information, qr_information)


            #cv2.imshow('ROBOT POV', image)
            #if cv2.waitKey(1) == 0xFF: 
            #        return  # esc to quit
            return image
            
            



    def __init__(self, detector, decider, qr_detector, localisation, HOST, PORT):

        
        self.HOST = HOST
        self.PORT = PORT
        self.differences = []

        self.detector = detector
        self.decider = decider
        self.qr_detector = qr_detector
        self.localisation = localisation

        self.received_data = b"" 

    def bind_socket(self):

        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # Bind the socket to the host and port
            s.bind((self.HOST, self.PORT))

            print("listening")

            # Listen for incoming messages on the socket
            s.listen()

            

            # Accept the message on the socket, addr = the client host and port, conn = the connection.
            conn, addr = s.accept()

            print("connected")

            
            self.run(conn, s)

            print(self.differences)
            
            
    def draw_arrow(self, orientation, bounding_box_width, bounding_box_height, image, center_x, center_y):

        if orientation is None: return
        orientation = (orientation * -1) + 90 # convert to angle used in function (0 is right)

        # Calculate the endpoint of the arrow
        arrow_length = 50  # You can adjust the arrow length as needed

        # fix the arrow spawn

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
                
                received_data = self.receive_data(conn)
                parsed_data = self.parse_data(received_data)

                if parsed_data is None: 
                    continue

                image, self.movement_state, movement, rotation, ang = self.convert_bytes_to_image(parsed_data)

                format = '%H:%M:%S:%f'
                current_time = datetime.utcnow().strftime(format)[:-3]

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                image_information, qr_information = self.recognise_image(image)

                if image_information is not None and len(image_information) > 0:
                    self.draw_image_information(image_information[0], image)
                robot_movements, state, attack = self.process_information(image_information, qr_information)
                self.localisation.set_vels(movement, rotation, ang)


                cv2.imshow('ROBOT POV', image)
                if cv2.waitKey(1) == 0xFF: 
                        return  # esc to quit
                
                for movement in robot_movements:
                    self.send_response(conn, movement, state, attack)




    
    def draw_image_information(self, image_information, image):
        print(image_information)
        (x1, y1, x2, y2) = image_information["position"]
        orientation = image_information["orientation"]
        bounding_box_area = image_information["bounding_box_area"]

        # Calculate the width and height of the bounding box
        width = x2 - x1
        height = y2 - y1

        center_x = (x1 + x2) / 2
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
        opponent_information = self.detector.run(image)
        return opponent_information, qr_information

    def process_information(self, image_information, qr_information):
        """
        Pass information gathered about an image to the decision making model.
        image_information: The information about the image.
        """
        
        robot_movements, state, attack = self.decider.run(image_information, qr_information, self.localisation.position)

        return robot_movements, state, attack



            
    def receive_data(self, conn):
        # Initialize an empty byte string to accumulate data
        

        while True:
            # Receive 1024 bytes of data
            data = conn.recv(1024)
            
            # If the message delimiter is in the message, the end of the message has been found
            if b'\n' in data:
                # Split the data at the newline, keeping part before the newline and the remainder
                complete_message, leftover_data = data.split(b'\n', 1)
                message = self.received_data + complete_message
                self.received_data = leftover_data
                return message
            
            # Append the newly received data to the current item of data being collected
            self.received_data += data  


    def parse_data(self, received_data):
        try:
            # Attempt to parse the message with JSON. Agreed encoding = UTF8
            parsed_data = json.loads(received_data.decode('utf-8'))
            return parsed_data
        except Exception as e:
            print(e)
            
            print("failed to parse")

    

    def convert_bytes_to_image(self, parsed_data):
        # Retrieve the screenshot field of the JSON message
        image_data_byte_array = parsed_data['screenshotPNG']

        if self.PORT == 9999:
            import base64
            image_data_byte_array = base64.b64decode(image_data_byte_array)

        # Create a BytesIO object to work with the image data
        image_stream = io.BytesIO(bytes(image_data_byte_array))



        # Open the image using PIL (Pillow)
        image = Image.open(image_stream)

        # PIL images into NumPy arrays
        image = np.array(image)

        if self.PORT == 9999:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        state = parsed_data['movementState']

        movement = parsed_data['movement']
        rotation = parsed_data['rotation']
        ang = parsed_data["angle"]

        

        return image, state, movement, rotation, ang

    """def save_image(image):
        # Define a filename for the saved PNG image
        filename = 'computer_vision/saved_image.png'

        # Save the image as a PNG file
        image.save(filename, 'PNG')"""



    def send_response(self, conn, robot_movements, state, attack):

        success_response = {"status": "success", "movements": robot_movements, "state": state, "attack": attack}
        print(f"sending: {success_response}")
        conn.send(json.dumps(success_response).encode('utf-8') + b'\n')
