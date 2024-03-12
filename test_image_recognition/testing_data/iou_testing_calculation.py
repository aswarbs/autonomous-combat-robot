import csv
import numpy as np
import cv2
import os
import json
from predict_qr import DetectQR

def get_data_from_coco(path, frame_len):
    # Initialize an empty list to store the data
    data_array = []

    f = open(path)

    json_data = json.load(f)

    annotations = json_data["annotations"]

    # for annotation in annotations:
    #     print(annotation)


    # Assuming 'annotations' is a list of dictionaries with 'image_id' and 'bbox' keys
    # First, find the maximum 'image_id' value
    max_image_id = max(annotation['image_id'] for annotation in annotations)

    print(f"max image:{max_image_id}")

    # Initialize an empty dictionary to hold the bounding boxes grouped by 'image_id'
    annotation_dict = {}

    # Populate the dictionary
    for index in range(1, frame_len+1): 
        annotation_dict[index] = [annotation['bbox'] for annotation in annotations if annotation['image_id'] == index]


    data_array = [[key, val] for key, val in annotation_dict.items()]

    for x in range(len(data_array)):
         for y in range(len(data_array[x][1])):
            data_array[x][1][y][2] = int(data_array[x][1][y][0] + data_array[x][1][y][2])
            data_array[x][1][y][3] = int(data_array[x][1][y][1] + data_array[x][1][y][3])


    # Now, data_array contains the contents of the CSV file as a list of lists
    return data_array

def get_data_from_csv(path):
    # annotations are stored in csv
    # if an image has no annotation, there is nothing stored for the image
    # annotations are stored [image, xmin, ymin, xmax, ymax]

    # Initialize an empty list to store the data
    data_array = []

    # Read the CSV file and populate the data_array
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Skip the header row if it exists
        header = next(csv_reader, None)

        for row in csv_reader:
            data_array.append(row)

    # Now, data_array contains the contents of the CSV file as a list of lists
    return data_array

def get_iou(ground_truth, pred):
        # Retrieve ground truth and prediction arrays. remove the title element from the arrays.

        ground_truth = [float(element) for element in ground_truth]
        pred = [float(element) for element in pred]

        # coordinates of the area of intersection.
        ix1 = np.maximum(ground_truth[0], pred[0])
        iy1 = np.maximum(ground_truth[1], pred[1])
        ix2 = np.minimum(ground_truth[2], pred[2])
        iy2 = np.minimum(ground_truth[3], pred[3])
        
        # Intersection height and width.
        i_height = np.maximum(iy2 - iy1 + 1, np.array(0.))
        i_width = np.maximum(ix2 - ix1 + 1, np.array(0.))
        
        area_of_intersection = i_height * i_width
        
        # Ground Truth dimensions.
        gt_height = ground_truth[3] - ground_truth[1] + 1
        gt_width = ground_truth[2] - ground_truth[0] + 1
        
        # Prediction dimensions.
        pd_height = pred[3] - pred[1] + 1
        pd_width = pred[2] - pred[0] + 1
        
        area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection
        
        iou = area_of_intersection / area_of_union
        
        return iou

def get_iou_array(ground_truth_array, pred_array, frame_len, path):
     """
     iterate through both arrays
     compare the image names

     if an image appears in ground truth but not pred, the cv model fails to recognise the image (true negative)
     if an image appears in pred but not ground truth, the cv model has recognised an incorrect image (false positive)

     if either of these happen, compare the image names to find which is behind, and iterate through until they are the same
     """

     with os.scandir(path) as it:
          
          cnt = 0

          for entry in it:
               frame = cv2.imread(entry.path)
               ground_truth = ground_truth_array[cnt][1]
               pred = pred_array[cnt][1]

               for truth in ground_truth:
                    cv2.rectangle(frame, (int(truth[0]), int(truth[1])), (int(truth[2]), int(truth[3])), color=(255,0,0), thickness=1, lineType=cv2.LINE_AA)
                
               for p in pred:
                    cv2.rectangle(frame, (int(p[0]), int(p[1])), (int(p[2]), int(p[3])), color=(0,0,255), thickness=1, lineType=cv2.LINE_AA)

                # if a ground truth intersects with a pred get the iou
                
                # TODO ^^

               cv2.imshow("", frame)

               cv2.waitKey(0)

               cnt+=1
               
    
    
     

path = "testing_data/qr/output_images"
detect_qr = DetectQR(path)
preds, frame_len = detect_qr.find_qrs_and_distances()

ground_truth_path = r"testing_data/qr/csvs/coco_moving_qr_annotations.json"
ground_truth_data = get_data_from_coco(ground_truth_path, frame_len)

ious = get_iou_array(ground_truth_data, preds, frame_len, path)

