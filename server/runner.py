from computer_vision.detect_rubik import ObjectDetection
from computer_vision.detect_qr import DetectQR
from computer_vision.localisation import Localisation
from decision_making.decision_maker import DecisionMaker
from server_communication import ServerCommunication
import threading


# SIM
HOST = "127.0.0.1"
PORT = 2345



"""
# REAL
HOST = "192.168.0.14"
PORT = 9999
"""
 

if __name__ == "__main__":
    localisation = Localisation()
    qr_detector = DetectQR(localisation)
    
    detector = ObjectDetection()
    qr_detector = DetectQR(localisation)
    decision_maker = DecisionMaker(localisation.boundary_corners, localisation)

    server = ServerCommunication(detector, decision_maker, qr_detector, localisation, HOST, PORT)

    server_thread = threading.Thread(target=server.bind_socket)
    server_thread.start()
    

    while True: 
       localisation.root.update()
