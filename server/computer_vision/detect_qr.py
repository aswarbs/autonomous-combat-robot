
import cv2
import numpy as np
import sympy as sym
from pyzbar import pyzbar
import math

class DetectQR:


   

    def __init__(self, localisation):
        self.KNOWN_WIDTH = 342 # centimeters
        self.FOCAL_WIDTH = 50 # centimeters
        self.localisation = localisation
        self.offset = self.localisation.border_width



        self.orientation = math.pi/2

        self.arena_width = 250
        self.arena_height = 250
        self.qr_width = 30

        self.position = (int(self.arena_width / 2),int(self.arena_height / 2))

        self.lower_bound_x = 0
        self.lower_bound_y = 0
        self.upper_bound_x = self.arena_width
        self.upper_bound_y = self.arena_height

        self.arena_offset = 0 # arena is shifted 25 to the left

        self.top_left_boundary = (self.arena_offset,self.arena_height + self.arena_offset)
        self.top_right_boundary = (self.arena_width + self.arena_offset, self.arena_height + self.arena_offset)
        self.bottom_left_boundary = (self.arena_offset,self.arena_offset)
        self.bottom_right_boundary = (self.arena_width + self.arena_offset,self.arena_offset)

        self.top_left_facing_south_position = (15, 0)
        self.top_left_facing_east_position = (0, 15)

        self.top_right_facing_south_position = (235, 0)
        self.top_right_facing_west_position = (250, 15)

        self.bottom_left_facing_north_position = (15, 250)
        self.bottom_left_facing_east_position = (0, 15)

        self.bottom_right_facing_north_position = (235, 250)
        self.bottom_right_facing_west_position = (250, 235)

        self.time_difference = 0
        self.velocity = 0
        self.angular_velocity = 0
        self.robot_size = 9
        self.border_width = 10

        self.frame_rate = 0.1

        self.labels_to_coordinates = {
            "top_left_facing_south": self.top_left_facing_south_position,
            "top_left_facing_east": self.top_left_facing_east_position,
            "top_right_facing_south": self.top_right_facing_south_position,
            "top_right_facing_west": self.top_right_facing_west_position,
            "bottom_left_facing_north": self.bottom_left_facing_north_position,
            "bottom_left_facing_east":  self.bottom_left_facing_east_position,
            "bottom_right_facing_north": self.bottom_right_facing_north_position,
            "bottom_right_facing_west": self.bottom_right_facing_west_position
        }





    def triangulate_position(self, p1, p2, d1, d2):
        x,y = sym.symbols('x,y')
        eq1 = sym.Eq((x - p1[0])**2 + (y - p1[1])**2, d1**2)
        eq2 = sym.Eq((x - p2[0])**2 + (y - p2[1])**2, d2**2)
        results = sym.solve([eq1,eq2],(x,y))

        valid_results = []

        for x,y in results:

            if (not x.is_real) or (not y.is_real):
                return
            
            if x < self.lower_bound_x or x > self.upper_bound_x:
                continue
            if y < self.lower_bound_y or y > self.upper_bound_y:
                continue
            valid_results.append((int(x), int(y)))

        if(len(valid_results) == 0):
            return

        assert(len(valid_results) == 1)

        result = valid_results[0]
        return result
    

    def calculate_width(self, points):

        # Calculate Euclidean distance between points
        dist_1 = np.linalg.norm(points[1] - points[3])  # Distance between point 0 and point 1
        dist_2 = np.linalg.norm(points[2] - points[4])  # Distance between point 1 and point 2

        # Take the average of the distances to estimate the width
        width = (dist_1 + dist_2) / 2.0
        return width



    def find_position(self, labels_to_distances):

        points = []
        distances = []

        for key, value in labels_to_distances.items():
            points.append(self.labels_to_coordinates[key])
            distances.append(value)

        triangulation = self.triangulate_position(points[0], points[1], distances[0], distances[1])

        if(triangulation is None):
            return 
        
        position = (self.border_width + triangulation[0],self.border_width + (self.arena_height - triangulation[1]))

        return position
             

        
    
    def find_qrs_and_distances(self, frame):
        
        distances = []
        labels_to_distances = {}

        decoded_info_list = pyzbar.decode(frame, [pyzbar.ZBarSymbol.QRCODE,])
        # Put the text on the image
        for decoded_info in decoded_info_list:

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
            #self.localisation.find_position(labels_to_distances)
            position = self.find_position(labels_to_distances)
            if position is not None:
                cv2.putText(frame, f"position: {position[0]} {position[1]}", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        return labels_to_distances