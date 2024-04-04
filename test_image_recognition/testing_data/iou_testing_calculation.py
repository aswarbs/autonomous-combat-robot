

import csv
import numpy as np
import cv2
import os
import json
from predict_rubik import ObjectDetection
from shapely.geometry import Polygon

i2l = {
     1: "cube",
     2: "red",
     3: "orange",
     4: "yellow",
     5: "green",
     6: "blue",
     7: "white"
}     

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
        annotation_dict[index] = []
        for annotation in annotations:
             if annotation['image_id'] == index:
                  if annotation['segmentation'] == []:
                    found = annotation['bbox']
                    found = [[found[0], found[1], found[0] + found[2], found[1], found[0] + found[2], found[1] + found[3], found[0], found[1] + found[3]]]
                    annotation_dict[index].append([found, i2l[annotation['category_id']]])
                  else:
                    annotation_dict[index].append([annotation['segmentation'], i2l[annotation['category_id']]])
        for item in annotation_dict[index]:
            print(item)


    data_array = [[key, val] for key, val in annotation_dict.items()]

    for x in range(len(data_array)):
         for y in range(len(data_array[x][1])):
            
            if data_array[x][1][y][0] == []: continue

            data_array[x][1][y][0] = [[int(data_array[x][1][y][0][0][0]), int(data_array[x][1][y][0][0][1])], [int(data_array[x][1][y][0][0][2]), int(data_array[x][1][y][0][0][3])],  [int(data_array[x][1][y][0][0][4]), int(data_array[x][1][y][0][0][5])],  [int(data_array[x][1][y][0][0][6]), int(data_array[x][1][y][0][0][7])]]


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

def get_iou(polygon1, polygon2):
    
    intersect = polygon1.intersection(polygon2).area
    union = polygon1.union(polygon2).area
    iou = intersect / union
    print(iou)  
    return iou

def intersects(rec1, rec2):
    return not (rec1[2] < rec2[0]
                or rec1[0] > rec2[2]
                or rec1[1] > rec2[3]
                or rec1[3] < rec2[1])

def get_iou_array(ground_truth_array, pred_array, frame_len, path):
     """
     iterate through both arrays
     compare the image names

     if an image appears in ground truth but not pred, the cv model fails to recognise the image (true negative)
     if an image appears in pred but not ground truth, the cv model has recognised an incorrect image (false positive)

     if either of these happen, compare the image names to find which is behind, and iterate through until they are the same
     """

     ious = []
     segments = []

     print(pred_array)

     cnt = 0
     for p in preds:
        if(p[1] != []):
             cnt+=1
     print(f"pred count: {cnt}")

     cnt = 0
     for p in ground_truth_array:
        if(p[1] != []):
             cnt+=1
     print(f"pred count: {cnt}")


          

     with os.scandir(path) as it:
          
          cnt = -1

          #print(preds)

          print(ground_truth_array)

          for entry in it:
               cnt+=1
               print("here")
               print(f"cnt: {cnt}")
               frame = cv2.imread(entry.path)
               ground_truth = ground_truth_array[cnt]
               pred = pred_array[cnt]
               if pred[1] == []:
                    print(f"exited: {pred}")
                    continue
               pred[1] = pred[1][0]
               

               ground_truth = ground_truth[1]
               pred = pred[1]

               for truth in ground_truth:
                    colour = truth[1]
                    coords = truth[0]

                    print(f"truth colour: {colour}")
                    print(f"truth coords: {coords}")

                    if coords == []: continue

                    pts = np.array(coords,np.int32)
                    
                    cv2.polylines(frame, [pts], True, (203,192,255), 2)
                    cv2.putText(frame, colour, coords[0], cv2.FONT_HERSHEY_COMPLEX, 1, (203,192,255), 1, cv2.LINE_AA, False)

                    colour_counter = 0
                    
                    for p in pred:
                            pcolour = p[1]
                            pcoords = p[0]

                            print(f"p colour: {pcolour}")
                            print(f"p coords: {pcoords}")
                                    
                            pts = np.array(pcoords,np.int32)

                            colours = [0,0,0]
                            colours[colour_counter % 3] = 255
                            colour_counter += 1
                            
                            cv2.polylines(frame, [pts], True, tuple(colours), 2)
                            cv2.putText(frame, pcolour, pcoords[0], cv2.FONT_HERSHEY_COMPLEX, 1, tuple(colours), 1, cv2.LINE_AA, False)
                            
                            tuple_truth = tuple(tuple(inner_list) for inner_list in coords)
                            tuple_pred = tuple(tuple(inner_list) for inner_list in pcoords)

                            if len(tuple_pred) < 3:
                                 continue
                            
                            polygon1 = Polygon(tuple_truth)
                            polygon2 = Polygon(tuple_pred)

                            intersect = polygon1.intersection(polygon2).area

                            if (intersect == 0):
                                 continue
                            
                            print(f"colour: {colour} pcolour: {pcolour}")
                            if colour == 'cube' or pcolour == 'cube':
                              # ignore
                              pass
                            else:
                                segments.append(colour == pcolour)
                              
                            if colour == pcolour:
                              iou = get_iou(polygon1, polygon2)
                              ious.append(iou)




               frame = cv2.resize(frame, (900, 600))
               cv2.imshow("", frame)

               cv2.waitKey(0)

     print(f"mean: {np.mean(ious)}")
     print(f"stddev: {np.std(ious)}")
     print(f"correct segs: {sum(segments) / len(segments)}")

               
    
     
# Specify the folder path containing the images
image_folder = r'test_image_recognition\testing_data\rubik\output_real_faces'

# Create a list of image files in the folder
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.png'))]

detect_rubik = ObjectDetection()

preds = []

cnt = 1

ground_truth_path = r"test_image_recognition\testing_data\rubik\csvs\real_cubes.json"
ground_truth_data = get_data_from_coco(ground_truth_path, len(image_files))

for f in image_files:

    f = cv2.imread(f)
    contours_dict = detect_rubik.run(f, cnt)
    print(f"after execution: {contours_dict}")
    preds.append(contours_dict)

    cnt += 1
    



ious = get_iou_array(ground_truth_data, preds, len(image_files), r"test_image_recognition\testing_data\rubik\output_real_faces")