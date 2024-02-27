from computer_vision.detect_rubik import ObjectDetection
from computer_vision.detect_qr import DetectQR
from computer_vision.localisation import Localisation
from decision_making.decision_maker import DecisionMaker
from server_communication import ServerCommunication
import threading

if __name__ == "__main__":
    localisation = Localisation()


    detector = ObjectDetection()
    qr_detector = DetectQR(localisation)
    decision_maker = DecisionMaker()

    

    server = ServerCommunication(detector, decision_maker, qr_detector, localisation)

    server_thread = threading.Thread(target=server.bind_socket)
    server_thread.start()

    

    while True: 
        localisation.root.update()

    