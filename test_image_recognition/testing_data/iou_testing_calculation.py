import numpy as np

def get_ground_truth_data(self, path):
    # ground truth:
    # annotations are stored in csv: vott_output/vott_csv_export/rubiks_sim-export.csv
    # if an image has no annotation, there is nothing stored for the image
    # annotations are stored [image, xmin, ymin, xmax, ymax, label]
    pass

def get_prediction_data(self, path):
    # prediction data:
    # need to run folder through computer vision model in detect_rubik
    # save bounding boxes in the same format as ground truth
    pass

def get_iou(ground_truth, pred):
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