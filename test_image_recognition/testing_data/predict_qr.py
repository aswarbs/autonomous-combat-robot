
import cv2
import os
from pyzbar import pyzbar

class DetectQR:
   

    def __init__(self, path):
        self.KNOWN_WIDTH = 225 # centimeters
        self.FOCAL_WIDTH = 36 # centimeters
        self.path=path


        
    
    def find_qrs_and_distances(self):

        cnt = 0

        arr = []

        with os.scandir(self.path) as it:
            for entry in it:
                if entry.name.endswith(".jpg") and entry.is_file():

                    cnt+=1

                    current_arr = []


                    frame = cv2.imread(entry.path)
                    


                    codes = pyzbar.decode(frame, [pyzbar.ZBarSymbol.QRCODE,])
                    for code in codes:
                        
                        label = code.data.decode()
                        left = code.rect.left
                        top = code.rect.top
                        width = code.rect.width
                        height = code.rect.height

                        if left < 0: left = 0
                        if top < 0: top = 0

                        points = [left, top, left + width, top + height]

                        current_arr.append(points)

                    arr.append([cnt, current_arr])

        return arr, cnt
            


path = "testing_data/qr/output_images"
detect_qr = DetectQR(path)
detect_qr.find_qrs_and_distances()