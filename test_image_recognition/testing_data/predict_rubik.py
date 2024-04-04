
import cv2
from ultralytics import YOLO
import numpy as np
import os





class ObjectDetection():

    # Initialise the Object Detection Object
    def __init__(self):

        # Load the model
        self.model = self.load_model()

        self.class_names = self.model.model.names

        self.COLOUR_RANGES = {
            #'white': [[255, 255, 255], [0, 0, 230]],
            'red1': [[5,255,255], [0, 100, 100]],
            'red2':[[179,255,255], [170, 100, 100]],
            'green': [[89, 255, 255], [55, 100, 100]],
            'blue': [[128, 255, 255], [90, 50, 50]],
            #'yellow': [[35, 255, 255], [25, 100, 100]],
            'orange': [[30, 255, 255], [6, 100, 100]],
        }

        self.model(None)

        



        
        
    # load the desired model
    def load_model(self):
        model = YOLO(os.getcwd() + r'\server\computer_vision\runs\detect\yolov8n_v8_50e32\weights\best.pt')
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

        confident_bounding_boxes = []
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
                    confident_bounding_boxes += bounding_box

        return screenshot, confident_bounding_boxes
    
    def detect_whole_color_contour(self, roi, count, x1, y1, x2, y2):

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

            print(f"number of contours: {len(contours)}")

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


        for key, value in contours_dict.items():
            val = value.tolist()
            for index, v in enumerate(val):
                val[index] = v[0]
                val[index][0] += x1
                val[index][1] += y1

            
            contours_dict[key] = val 


        data_array = [[val, key] for key, val in contours_dict.items()]

        

        return data_array
    
            
    def refine_mask(self, mask):

        # Apply closing to fill the gap between adjacent white regions
        kernel = np.ones((30, 30), np.uint8)  # Adjust the kernel size as needed
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        return mask

    def run(self, screenshot, count):

        # Retrieve the results from the training model detecting where the Rubik's cubes are in the image.
        results = self.predict(screenshot)
        

        # Create an empty dictionary to store information about each Rubik's cube
        contours = [count, []]

         # retrieve the image with the bounding boxes drawn, and the location of the bounding boxes, from the screenshot
        frames, bounding_boxes = self.draw_bounding_boxes(results, screenshot)
        #contours[1].append(bounding_boxes)
        print(f"bounding box: {bounding_boxes}")

        # For every object detected in the image.
        for idx, box in enumerate(bounding_boxes):
            # Retrieve the coordinates of the current bounding box
            x1, y1, x2, y2 = box.xyxy[0]

            box = np.array([[x1, y1], [x2,y1], [x2,y2], [x1, y2]], np.int32)

            l = []

            l.append([box, 'cube'])

            # Convert the coordinates to integers
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Crop the region of interest
            roi = screenshot[y1:y2, x1:x2]

            # Send the cropped image to a colour recognition function to retrieve the colours of the sides of the Rubik's cube.
            contour = self.detect_whole_color_contour(roi, count, x1, y1, x2, y2)
            for c in contour:
                l.append(c)

            contours[1].append(l)

        return contours

