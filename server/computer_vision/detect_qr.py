
import cv2
import numpy as np
import sympy as sym
from pyzbar import pyzbar

class DetectQR:
   

    def __init__(self, localisation):
        self.KNOWN_WIDTH = 225 # centimeters
        self.FOCAL_WIDTH = 36 # centimeters
        self.localisation = localisation
        self.offset = self.localisation.border_width



    def calculate_width(self, points):
        # Calculate Euclidean distance between points
        dist_1 = np.linalg.norm(points[1] - points[2])  # Distance between point 0 and point 1
        dist_2 = np.linalg.norm(points[3] - points[4])  # Distance between point 1 and point 2

        # Take the average of the distances to estimate the width
        width = (dist_1 + dist_2) / 2.0
        return width



             

        
    
    def find_qrs_and_distances(self, frame):
        
        distances = []
        labels_to_distances = {}

        decoded_info_list = pyzbar.decode(frame, [pyzbar.ZBarSymbol.QRCODE,])
        # Put the text on the image
        for decoded_info in decoded_info_list:

            print(f"{decoded_info.data.decode()} {decoded_info.rect.left} {decoded_info.rect.top} {decoded_info.rect.width} {decoded_info.rect.height}")

            label = decoded_info.data.decode()

            left = decoded_info.rect.left
            top = decoded_info.rect.top
            width = decoded_info.rect.width
            height = decoded_info.rect.height

            if left < 0: left = 0
            if top < 0: top = 0

            points = [label, left, top, left + width, top + height]

            cv2.rectangle(frame, (points[1], points[2]), (points[3], points[4]), color=(255,0,0), thickness=1, lineType=cv2.LINE_AA)
            
            cv2.putText(frame, label, (points[1], points[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            
            width = self.calculate_width(points)
            

            approx_distance = (self.KNOWN_WIDTH * self.FOCAL_WIDTH) / width # in centimeters
            approx_distance = round(approx_distance, 3)

            distances.append(approx_distance)

            print(f"qr distance: {approx_distance}")
            cv2.putText(frame, str(approx_distance), (points[3], points[4]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            labels_to_distances[label] = approx_distance

            
        if(len(labels_to_distances)) == 2:
            self.localisation.find_position(labels_to_distances)

        return labels_to_distances