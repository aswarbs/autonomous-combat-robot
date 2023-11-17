# detect the rubiks cube in the image
# draw a bounding box around the rubiks cube in the image

import csv
import cv2
from ultralytics import YOLO
import math
import os
import numpy as np

# Specify the folder path containing the images
#image_folder = r'computer_vision\datasets\rubiks_cube_model\test\images'
"""image_folder = r'test_image_recognition\testing_data\output_images'

# Create a list of image files in the folder
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.png'))]
"""
class ObjectDetection():

    # Initialise the Object Detection Object
    def __init__(self):

        # Load the model
        self.model = self.load_model()

        self.class_names = self.model.model.names

        self.COLOUR_RANGES = {
            'white': [[172, 30, 230], [0, 0, 100]],
            'red1': [[10,255,255], [0, 150, 150]],
            'red2':[[179,255,255], [160, 150, 150]],
            'green': [[89, 255, 255], [55, 100, 100]],
            'blue': [[128, 255, 255], [90, 100, 100]],
            'yellow': [[35, 255, 255], [25, 150, 100]],
            'orange': [[23, 255, 255], [15, 150, 150]],
        }

        


    def calculate_absolute_orientation(self, orientation, most_prominent_side):

        if(most_prominent_side == "blue"):
            return orientation
        elif(most_prominent_side == "green"):
            return (180 - orientation) * -1
        elif(most_prominent_side == "white"):
            return orientation - 90
        elif(most_prominent_side == "yellow"):
            return orientation + 90
        else:
            print("invalid colour!!")
            return
        
    def draw_arrow(self, orientation, bounding_box_width, bounding_box_height, image):
         # Retrieve the orientation of the Rubik's Cube (you should replace this with your actual orientation value)
        orientation = (orientation * -1) + 90 # convert to angle used in function (0 is right)

        # Calculate the endpoint of the arrow
        arrow_length = 50  # You can adjust the arrow length as needed

        center_x = bounding_box_width / 2
        center_y = bounding_box_height / 2


        arrow_endpoint_x = int(center_x + arrow_length * math.cos(math.radians(orientation)))
        arrow_endpoint_y = int(center_y + arrow_length * math.sin(math.radians(orientation)))

        cv2.arrowedLine(image, ((int)(center_x), (int)(center_y)), (arrow_endpoint_x, arrow_endpoint_y), (0, 0, 255), 2)

        
        
    # load the desired model
    def load_model(self):
        model = YOLO(r'server\computer_vision\runs\detect\yolov8n_v8_50e32\weights\best.pt')
        # model.fuse()
        return model
    
    # predict whether the image fits the model
    def predict(self, screenshot):
        results = self.model(screenshot)
        return results
    
    """
    Use the results of the deep learning model to draw bounding boxes around the recognised items in the image.

    results: the results of the deep learning model.
    screenshot: the current image to draw bounding boxes over.
    """
    def draw_bounding_boxes(self, results, screenshot):
        # For every result,
        for result in results:
            # Retrieve the current bounding box predictions
            bounding_boxes = result.boxes
            # For each box in the list of bounding boxes,
            for bounding_box in bounding_boxes:
                # Retrieve the coordinates of the current bounding box
                x1, y1, x2, y2 = bounding_box.xyxy[0]
                # Convert the coordinates to integers
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # Calculate the width
                width = x2-x1
                # Calculate the height
                height = y2-y1

                # Retrieve the class name index (what the object is)
                class_name = int(bounding_box.cls[0])
                # Retrieve the current class from the class name index
                current_class = self.class_names[class_name]

                # Retrieve the confidence score
                confidence_score = bounding_box.conf[0]

                # If the algorithm is reasonably confident,
                if confidence_score > 0.5:
                    
                    # Display a bounding box over the detected object.
                    
                    cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 0, 0), 1)
                    pass    

        return screenshot, bounding_boxes
    
    def detect_whole_color_contour(self, roi):

        # Convert the isolated face to the HSV color space for better color filtering
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        contours_dict = {}  # Create a dictionary to store contours and their colors

        for color, ranges in self.COLOUR_RANGES.items():

            # Define the HSV range for the desired face color
            lower = np.array(ranges[1], dtype=np.uint8)
            upper = np.array(ranges[0], dtype=np.uint8)

            # Create a mask to isolate the target color
            mask = cv2.inRange(hsv, lower, upper)

            mask = self.refine_mask(mask)

            
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                largest_contour = max(contours, key=cv2.contourArea)
                # Approximate the contour with a polygon
                epsilon = 0.02 * cv2.arcLength(largest_contour, True)
                approx_polygon = cv2.approxPolyDP(largest_contour, epsilon, True)
                approx_polygon = cv2.convexHull(approx_polygon)

                # Add the largest face contour and its color to the dictionary
                contours_dict[color] = approx_polygon


        if "red1" in contours_dict and "red2" in contours_dict:
            merged_red_contour = np.vstack((contours_dict["red1"], contours_dict["red2"]))

            # Find the convex hull of the merged contours
            merged_red_contour = cv2.convexHull(merged_red_contour)

            # Add the merged "red" contour to the dictionary
            contours_dict["red"] = merged_red_contour

            del contours_dict["red1"]
            del contours_dict["red2"]

        if("red1" in contours_dict):
            contours_dict["red"] = contours_dict["red1"]
            del contours_dict["red1"]

        if("red2" in contours_dict):
            contours_dict["red"] = contours_dict["red2"]
            del contours_dict["red2"]

        for contour in contours_dict:
            cv2.drawContours(roi, [contours_dict[contour]], -1, (255, 0, 0), 2)

        return contours_dict
    

    """
    from a dictionary of contours, 
    approximate the orientation of the cube.
    """
    def calculate_orientation_from_contours(self, contours_dict):

        # Convert the dictionary of contours into a list of (name, contour) pairs
        contours_list = [(name, contour) for name, contour in contours_dict.items()]


        # Sort the list of (name, area) pairs by area in descending order
        contours_list.sort(key=lambda x: cv2.contourArea(x[1]), reverse=True)


        # Extract the names of the two largest contours
        largest_contours = contours_list[:2]

        # Calculate the areas and bounding rectangles of each contour
        contour_info = []

        for name, contour in largest_contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            contour_info.append((name, area, x))

        # Sort the list of (name, area, x) pairs by X-coordinate in ascending order
        contour_info.sort(key=lambda x: x[2])

        # The contour with the smallest X-coordinate is the leftmost, and the one with the largest X-coordinate is the rightmost
        leftmost_contour = contour_info[0]
        rightmost_contour = contour_info[-1]

        

        # use this to estimate the orientation

        if(leftmost_contour == rightmost_contour):
            left_area = 0
        else:
            left_area = leftmost_contour[1]

        right_area = rightmost_contour[1]


        least_prominent_area = min(left_area, right_area)

        orientation = (least_prominent_area) / (left_area + right_area)

        if(left_area > right_area):
            orientation *= -1

        orientation = self.convert_orientation_to_degrees(orientation)

        print(f"most prominent side: {largest_contours[0][0]}.")
        print(f"orientation:{orientation}")
        print(f"orientation of blue: {self.calculate_absolute_orientation(orientation, largest_contours[0][0])}")



        return self.calculate_absolute_orientation(orientation, largest_contours[0][0])
    
    def convert_orientation_to_degrees(self, orientation):
        return orientation * 90

            
    def refine_mask(self, mask):

        # Apply closing to fill the gap between adjacent white regions
        kernel = np.ones((8, 8), np.uint8)  # Adjust the kernel size as needed
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        return mask

    def run(self, screenshot):
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # Retrieve the results from the training model detecting where the Rubik's cubes are in the image.
        results = self.predict(screenshot)

        # Create an empty dictionary to store information about each Rubik's cube
        rubiks_cubes_info = {}

         # retrieve the image with the bounding boxes drawn, and the location of the bounding boxes, from the screenshot
        frames, bounding_boxes = self.draw_bounding_boxes(results, screenshot)

        # For every object detected in the image.
        for idx, box in enumerate(bounding_boxes):
            # Retrieve the coordinates of the current bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            # Convert the coordinates to integers
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Crop the region of interest
            roi = screenshot[y1:y2, x1:x2]

            # Send the cropped image to a colour recognition function to retrieve the colours of the sides of the Rubik's cube.
            contours_dict = self.detect_whole_color_contour(roi)

            orientation = self.calculate_orientation_from_contours(contours_dict)

            # Calculate the width and height of the bounding box
            width = x2 - x1
            height = y2 - y1

            if orientation is not None:
                self.draw_arrow(orientation, width, height, roi)


            # Store information about the Rubik's cube in the dictionary
            rubiks_cubes_info[idx] = {
                "position": (x1, y1, x2, y2),
                "orientation": orientation,
                "bounding_box_area": width * height
            }

        # Show the resulting image with labelled colors
        cv2.imshow('Image', screenshot)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

        # Return the dictionary containing information for each Rubik's cube
        return rubiks_cubes_info
    
"""   def store_bounding_boxes_in_csv(self, image_files, csv_filename):
        # Create a list to store information about all bounding boxes
        all_bounding_boxes_info = []

        for image_file in image_files:
            # Convert the screenshot to BGR format if needed.
            screenshot = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_RGB2BGR)

            # Retrieve the results from the object detection model.
            results = self.predict(screenshot)

            # Retrieve the image with the bounding boxes drawn and the location of the bounding boxes.
            frames, bounding_boxes = self.draw_bounding_boxes(results, screenshot)

            # For every object detected in the image.
            for idx, box in enumerate(bounding_boxes):
                # Retrieve the coordinates of the current bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)

                file_name = os.path.basename(image_file)

                # Append bounding box coordinates to the list
                all_bounding_boxes_info.append([file_name, x1, y1, x2, y2])

        # Save all bounding box information to a single CSV file
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['image', 'xmin', 'ymin', 'xmax', 'ymax'])  # Write header
            csv_writer.writerows(all_bounding_boxes_info)

# Create an instance of the ObjectDetection class
od = ObjectDetection()

# Specify the CSV filename to store all bounding box information
csv_filename = r"test_image_recognition\testing_data\pred_bounding_boxes.csv"

# Process each image and store bounding box information in the same CSV file
od.store_bounding_boxes_in_csv(image_files, csv_filename)"""