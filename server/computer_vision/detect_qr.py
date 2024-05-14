
import cv2
import numpy as np
import sympy as sym
from pyzbar import pyzbar
import math
from functools import lru_cache

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

        self.top_left_facing_south_position = (15 + self.arena_offset, 0+ self.arena_offset)
        self.top_left_facing_east_position = (0+ self.arena_offset, 15+ self.arena_offset)

        self.top_right_facing_south_position = (235+ self.arena_offset, 0+ self.arena_offset)
        self.top_right_facing_west_position = (250+ self.arena_offset, 15+ self.arena_offset)

        self.bottom_left_facing_north_position = (15+ self.arena_offset, 250+ self.arena_offset)
        self.bottom_left_facing_east_position = (0+ self.arena_offset, 235+ self.arena_offset)

        self.bottom_right_facing_north_position = (235+ self.arena_offset, 250+ self.arena_offset)
        self.bottom_right_facing_west_position = (250+ self.arena_offset, 235+ self.arena_offset)

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

        result = valid_results[0]
        return result
    

    def calculate_width(self, points):

        # if you are directly in front of it the width == the height
        # if you are skewed then the width < the height
        # ratio of 1: direct
        # ratio of 1.5: width > height: never?
        # ratio of 0.5: width < height: skewed

        # Calculate Euclidean distance between points
        dist_1 = np.linalg.norm(points[1] - points[3])  # Distance between point 0 and point 1
        dist_2 = np.linalg.norm(points[2] - points[4])  # Distance between point 1 and point 2

        # Take the average of the distances to estimate the width
        width = (dist_1 + dist_2) / 2.0

        print(f"width: {dist_1}")
        print(f"height: {dist_2}")
        return width * (dist_2 / dist_1)



    def find_position(self, labels_to_distances, frame):

        points = []
        distances = []

        # print the distances

        for key, value in labels_to_distances.items():

            print(f"point: {self.labels_to_coordinates[key]}")
            print(f"distance: {value}")
            points.append(self.labels_to_coordinates[key])
            distances.append(value)

        triangulation = self.triangulate_position(points[0], points[1], distances[0], distances[1])

        if(triangulation is None):
            return 
        

        # this is it
        position = [triangulation[0], (self.arena_height - triangulation[1])]

        cv2.putText(frame, f"position: {triangulation[0]} {triangulation[1]}", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

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
            _width = decoded_info.rect.width
            _height = decoded_info.rect.height

            if left < 0: left = 0
            if top < 0: top = 0

            points = [label, left, top, left + _width, top + _height]

            cv2.rectangle(frame, (points[1], points[2]), (points[3], points[4]), color=(255,0,0), thickness=1, lineType=cv2.LINE_AA)
            
            cv2.putText(frame, label, (points[1], points[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            
            width = _height
            

            approx_distance = (self.KNOWN_WIDTH * self.FOCAL_WIDTH) / width # in centimeters
            approx_distance = round(approx_distance, 3)

            distances.append(approx_distance)

            print(f"qr distance: {approx_distance}")
            cv2.putText(frame, "distance: " + str(approx_distance), (points[3], points[4]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            labels_to_distances[label] = approx_distance

            

    

            
        if(len(labels_to_distances)) == 2:
            #self.localisation.find_position(labels_to_distances)
            position = self.find_position(labels_to_distances, frame)
            
            if position is not None:

                position[1] = 250 - position[1]
                position = tuple(position)

                #self.localisation.position = position
                #self.localisation.find_orientation(labels_to_distances)
                #cv2.putText(frame, f"position: {position[0]} {position[1]}", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        return labels_to_distances