# detect the rubiks cube in the image
# draw a bounding box around the rubiks cube in the image

import cv2
import torch
import cvzone
from ultralytics import YOLO
import math
from sort import *


class ObjectDetection():

    # Initialise the Object Detection Object
    def __init__(self):

        # Load the model
        self.model = self.load_model()

        self.class_names = self.model.model.names

        self.colour_ranges = {
            'white': [[180, 30, 255], [0, 0, 200]],
            'red1': [[10,255,255], [0, 150, 150]],
            'red2':[[179,255,255], [160, 150, 150]],
            'green': [[89, 255, 255], [55, 150, 150]],
            'blue': [[128, 255, 255], [90, 150, 150]],
            'yellow': [[35, 255, 255], [25, 150, 150]],
            'orange': [[20, 255, 255], [10, 150, 150]],
        }

    # load the desired model
    def load_model(self):
        model = YOLO(r'C:\Users\amber\Documents\Dissertation\autonomous-combat-robot\runs\detect\yolov8n_v8_50e32\weights\best.pt')
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
                    
                    #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 0, 0), 1)
                    pass    

        return screenshot, bounding_boxes
    
    def detect_whole_color_contour(self, roi):

        # Convert the isolated face to the HSV color space for better color filtering
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        contours_dict = {}  # Create a dictionary to store contours and their colors

        for color, ranges in self.colour_ranges.items():

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

        # find the largest contour in the contours_dict dictionary
        largest_color_contour = max(contours_dict, key=lambda k: cv2.contourArea(contours_dict[k]))
        print(largest_color_contour)

        largest_contour_area = contours_dict[largest_color_contour]


        # draw the largest contour
        for contour in contours_dict.values():
            cv2.drawContours(roi, [largest_contour_area], -1, (0, 255, 0), 2)

        

                


            
    def refine_mask(self, mask):

        # Apply closing to fill the gap between adjacent white regions
        kernel = np.ones((8, 8), np.uint8)  # Adjust the kernel size as needed
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        return mask

    
    # retrieve the image and run the model, output the image with bounding boxes
    def run(self, screenshot):
        # retrieve the results from the training model detecting where the rubiks cube/s are in the image.
        results = self.predict(screenshot)

        # retrieve the image with the bounding boxes drawn, and the location of the bounding boxes, from the screenshot
        frames, bounding_boxes = self.draw_bounding_boxes(results, screenshot)

        # initialise an array to store the colour labelled regions of interest.
        labelled_rois = []

        # for every object detected in the image.
        for box in bounding_boxes:
            # Retrieve the coordinates of the current bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            # Convert the coordinates to integers
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Crop the region of interest
            roi = screenshot[y1:y2, x1:x2]

            # send the cropped image to a colour recognition function to retrieve the colours of the sides of the rubiks cube.
            labelled_roi = self.detect_whole_color_contour(roi)

        # Show the resulting image with labelled colours
        cv2.imshow('Image', frames)


# Specify the folder path containing the images
image_folder = r'datasets\rubiks_cube_model\test\images'

# Create a list of image files in the folder
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.png'))]

# Create an instance of the ObjectDetection class
detector = ObjectDetection()

for image_file in image_files:
    try:
        # Read the image from the current file
        img = cv2.imread(image_file)
        
        # Run image recognition on the image
        detector.run(img)

        while True:
            # Wait for user input to move to the next image or quit
            key = cv2.waitKey(0)
            if key == ord('q'):
                cv2.destroyAllWindows()  # Close the current image window
                break
            elif key == ord('n'):
                break  # Move to the next image
    except Exception as e:
        print(e)


"""
img = r"test_image_recognition/saved_image.png"
image_file = cv2.imread(img)

detector.run(image_file)

while True:
    # Wait for user input to move to the next image or quit
    key = cv2.waitKey(0)
    if key == ord('q'):
        cv2.destroyAllWindows()  # Close the current image window
        break
    elif key == ord('n'):
        break  # Move to the next image
"""