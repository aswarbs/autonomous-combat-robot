
import cv2
import numpy as np
import sympy as sym

class DetectQR:
   

    def __init__(self, localisation):
        self.KNOWN_WIDTH = 225 # centimeters
        self.FOCAL_WIDTH = 36 # centimeters
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



             

        
    
    def find_qrs_and_distances(self, frame):
        
        distances = []

    
        retval, decoded_info, points, straight_qrcode = self.qcd.detectAndDecodeMulti(frame)

        decoded_info = [decoded_info[x] for x in range(len(decoded_info)) if decoded_info[x] != ""]

        if(points is not None and len(points) > 0 and decoded_info is not None and len(decoded_info) > 0):


            # Put the text on the image
            for x in range(len(decoded_info)):

                if(decoded_info[x] == ""):
                    continue

                points = np.array(points, np.int32)
                cv2.drawContours(frame, points, -1, (255, 0, 0), 2)
                cv2.putText(frame, decoded_info[x], points[x][0], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
                width = self.calculate_width(points[x])
                

                approx_distance = (self.KNOWN_WIDTH * self.FOCAL_WIDTH) / width # in centimeters
                approx_distance = round(approx_distance, 3)


                #self.localisation.position = position



                distances.append(approx_distance)
                cv2.putText(frame, str(approx_distance), points[x][2], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        if len(distances) == 0 or len(decoded_info) == 0:
            return
        # convert lists to dictionary
        labels_to_distances = {decoded_info[i]: distances[i] for i in range(len(decoded_info))}


        if(len(labels_to_distances)) == 2:
            self.localisation.find_position(labels_to_distances)

        return labels_to_distances