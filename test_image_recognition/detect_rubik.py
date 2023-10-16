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

    # load the desired model
    def load_model(self):
        model = YOLO('../yolo_weights/yolov8n.pt')
        # model.fuse()
        return model
    
    # predict whether the image fits the model
    def predict(self):
        results = self.model.train(
        data=r"C:\Users\amber\Documents\Dissertation\autonomous-combat-robot\datasets\rubiks_cube_model\data.yaml",
        imgsz=1280,
        epochs=50,
        batch=8,
        name='yolov8n_v8_50e'
        )
        #return results
    
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

                # Retrieve the class name
                class_name = int(bounding_box.cls[0])
                current_class = self.class_names[class_name]

                # Retrieve the confidence score
                confidence_score = bounding_box.conf[0]

                # If the algorithm is reasonably confident,
                if confidence_score > 0.5:
                    cvzone.putTextRect(screenshot, f'class: {current_class}', (x1,y1), scale=1, thickness=1, colorR = (0,0,255))
                    cvzone.cornerRect(screenshot, (x1, y1, width, height), l=9, rt=1, colorR=(255,0,255))
        return screenshot

    # retrieve the image and run the model, output the image with bounding boxes
    def run(self, screenshot):
        results = self.predict(img)
        frames = self.draw_bounding_boxes(results, img)

        cv2.imshow('Image', frames)

        if cv2.waitKey(1) == ord('q'):
            pass




detector = ObjectDetection()
detector.predict()

"""
while True:
    try:
        # Read the image from the file
        img = cv2.imread('test_image_recognition/saved_image.png')
        detector.run(img)
    except Exception as e:
        print(e)
"""