
import cv2
import os
from pyzbar import pyzbar

class DetectQR:
   

    def __init__(self, path):
        self.KNOWN_WIDTH = 225 # centimeters
        self.FOCAL_WIDTH = 36 # centimeters
        self.path=path


        self.qcd = cv2.QRCodeDetector()

        
    
    def find_qrs_and_distances(self):

        cnt = 0
        pyz_cnt = 0

        with os.scandir(self.path) as it:
            for entry in it:
                if entry.name.endswith(".jpg") and entry.is_file():


                    frame = cv2.imread(entry.path)
                    


                    codes = pyzbar.decode(frame, [pyzbar.ZBarSymbol.QRCODE,])
                    for code in codes:
                        print(f"{code.data.decode()} {code.rect.left} {code.rect.top} {code.rect.width} {code.rect.height}")
                        cnt += 1

                        
                    # Display the resulting frame
                    cv2.imshow('Frame',frame)

                    #cv2.waitKey(0)

        print(f"count: {cnt}")
            


path = "testing_data/qr/output_images"
detect_qr = DetectQR(path)
detect_qr.find_qrs_and_distances()