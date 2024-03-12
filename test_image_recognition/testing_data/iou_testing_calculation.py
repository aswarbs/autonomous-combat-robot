import csv
import numpy as np
import cv2

def get_data_from_coco(path):
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

def get_iou(box_arrs):
        # Retrieve ground truth and prediction arrays. remove the title element from the arrays.
        ground_truth = box_arrs[0][1:]
        pred = box_arrs[1][1:]

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

def get_iou_array(ground_truth_array, pred_array):
     """
     iterate through both arrays
     compare the image names

     if an image appears in ground truth but not pred, the cv model fails to recognise the image (true negative)
     if an image appears in pred but not ground truth, the cv model has recognised an incorrect image (false positive)

     if either of these happen, compare the image names to find which is behind, and iterate through until they are the same
     """

     
     # Create dictionaries to match items based on the first value
     ground_truth_dict = {item[0]: item for item in ground_truth_array}
     pred_dict = {item[0]: item for item in pred_array}

     # Initialize lists to store matched and unmatched items
     matched_items = []
     true_negative_arr = []
     false_positive_arr = []

    # Iterate through the first dictionary and check for matches in the second dictionary
     for key, value in ground_truth_dict.items():
         if key in pred_dict:
             matched_items.append((value, pred_dict[key]))
         else:
             true_negative_arr.append(value)

     # Iterate through the second dictionary and check for unmatched items
     for key, value in pred_dict.items():
         if key not in ground_truth_dict:
             false_positive_arr.append(value)

     ious = []

     # Print the results
     for item in matched_items:
          iou = get_iou(item)
          ious.append(iou)
          print(f"{item[0]}: {iou}")

     print("true negatives:", true_negative_arr)
     print("false positives:", false_positive_arr)

     
     image = cv2.imread("test_image_recognition/testing_data/output_images/frame_1.50.jpg")

     ground_truth = [(433, 319), (576, 428)]
     pred = [(425, 315), (581, 433)]


     cv2.rectangle(image, ground_truth[0], ground_truth[1], color=(0,0,255), thickness=1, lineType=cv2.LINE_AA)
     cv2.rectangle(image, pred[0], pred[1], color=(255,0,0), thickness=1, lineType=cv2.LINE_AA)

     cv2.imshow("", image)

     cv2.imwrite("0.83.jpg", image)


     cv2.waitKey(0)

     



ground_truth_path = r'test_image_recognition\testing_data\csvs\rubiks_sim_ground.csv'
prediction_path = r'test_image_recognition\testing_data\csvs\rubiks_sim_pred.csv'

ground_truth_data = get_data_from_csv(ground_truth_path)
prediction_data = get_data_from_csv(prediction_path)

ious = get_iou_array(ground_truth_data, prediction_data)

