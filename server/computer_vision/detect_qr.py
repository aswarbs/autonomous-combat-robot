
import cv2
import numpy as np
import math

class DetectQR:
   

    def __init__(self, localisation):
        self.KNOWN_WIDTH = 1650 # centimeters
        self.FOCAL_WIDTH = 15 # centimeters
        self.IMAGE_WIDTH = 517
        self.IMAGE_HEIGHT = 383
        self.QR_CODE_COORDINATE = 200
        self.localisation = localisation
        self.offset = self.localisation.border_width

        self.qcd = cv2.QRCodeDetector()


    def calculate_width(self, points):
        # Calculate Euclidean distance between points
        dist_1 = np.linalg.norm(points[0] - points[1])  # Distance between point 0 and point 1
        dist_2 = np.linalg.norm(points[1] - points[2])  # Distance between point 1 and point 2

        # Take the average of the distances to estimate the width
        width = (dist_1 + dist_2) / 2.0
        return width



    def calculate_position_from_object(self, distance, name):

        horizontal_distance = distance * math.cos(self.localisation.orientation)
        vertical_distance = distance * math.sin(self.localisation.orientation)

        if(name == "top_left"):
            position = (-self.QR_CODE_COORDINATE, self.QR_CODE_COORDINATE)
            return (position[0] + horizontal_distance + self.QR_CODE_COORDINATE + self.offset, position[1] - vertical_distance + self.QR_CODE_COORDINATE + self.offset)
        elif(name == "top_right"):
            position = (self.QR_CODE_COORDINATE,self.QR_CODE_COORDINATE)
            return (position[0] - horizontal_distance+ self.QR_CODE_COORDINATE + self.offset,  position[1] + vertical_distance+ self.QR_CODE_COORDINATE + self.offset)
        elif(name == "bottom_left"):
            position = (-self.QR_CODE_COORDINATE,-self.QR_CODE_COORDINATE)
            return (position[0] + horizontal_distance+ self.QR_CODE_COORDINATE + self.offset, position[1] + vertical_distance+ self.QR_CODE_COORDINATE + self.offset)
        elif(name == "bottom_right"):
            position = (self.QR_CODE_COORDINATE,-self.QR_CODE_COORDINATE)
            return (position[0] - horizontal_distance+ self.QR_CODE_COORDINATE + self.offset, position[1] + vertical_distance+ self.QR_CODE_COORDINATE + self.offset)
        else:
            print(f"qr code not found: {name}")
            return
        
        

             

        
    
    def find_qrs_and_distances(self, frame):
        
        print(f"image shape in qr: {frame.shape}")

        distances = []

    
        retval, decoded_info, points, straight_qrcode = self.qcd.detectAndDecodeMulti(frame)

        if(points is not None and len(points) > 0 and decoded_info is not None and len(decoded_info) > 0):


            # Put the text on the image
            for x in range(len(decoded_info)):
                points = np.array(points, np.int32)
                cv2.drawContours(frame, points, -1, (255, 0, 0), 2)
                cv2.putText(frame, decoded_info[x], points[x][0], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
                width = self.calculate_width(points[x])
                

                approx_distance = (self.KNOWN_WIDTH * self.FOCAL_WIDTH) / width # in centimeters
                approx_distance = round(approx_distance, 3)
                position = self.calculate_position_from_object(approx_distance, decoded_info[x])
                print(f"position of player: {position}")
                # mark it on the map


                self.localisation.position = position



                distances.append(approx_distance)
                cv2.putText(frame, str(approx_distance), points[x][2], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # convert lists to dictionary
        labels_to_distances = {decoded_info[i]: distances[i] for i in range(len(decoded_info))}

        # estimate the position based on distances and angles

        return labels_to_distances