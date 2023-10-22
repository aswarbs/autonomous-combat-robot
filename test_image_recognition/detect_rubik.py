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
            'white': [[180, 18, 255], [0, 0, 231]],
            'red': [[180, 255, 255], [159, 50, 70]],
            'green': [[89, 255, 255], [55, 100, 100]],
            'blue': [[128, 255, 255], [90, 200, 70]],
            'yellow': [[35, 255, 255], [25, 50, 70]],
            'orange': [[24, 255, 255], [10, 50, 70]],
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

        for colour, range in  self.colour_ranges.items():
            # Convert the isolated face to the HSV color space for better color filtering
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Define the HSV range for the desired face color
            lower = np.array(self.colour_ranges["green"][1], dtype=np.uint8)
            upper = np.array(self.colour_ranges["green"][0], dtype=np.uint8)

            # Create a mask to is   olate the target color
            mask = cv2.inRange(hsv, lower, upper)
            
            # Apply closing to fill the gap between adjacent white regions
            kernel = np.ones((10, 10), np.uint8)  # Adjust the kernel size as needed
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            cv2.imshow("mask", mask)

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            # Draw the grouped face contours on the original image
            cv2.drawContours(roi, contours, -1, (0, 0, 255), 2)

            if(contours is not None):
                return



    
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

        while True:
            if cv2.waitKey(1) == ord('q'):
                pass

# create an instance of the object detection class.
detector = ObjectDetection()


try:
    # Read the image from the file
    img = cv2.imread('test_image_recognition/saved_image.png')
    
    # run image recognition on the image
    detector.run(img)

except Exception as e:
    print(e)

"""
try:
    img = cv2.imread('test_image_recognition/saved_image.png')
    detector.run(img)
except Exception as e:
    print(e)
    """