from computer_vision.detect_rubik import ObjectDetection
from computer_vision.detect_qr import DetectQR
from computer_vision.localisation import Localisation
from decision_making.decision_maker import DecisionMaker
from server_communication import ServerCommunication
import threading
import time

def retrieve_from_queue():
    while True:
        if not server_queue.empty():
            vel, ang_vel = server_queue.get()
            localisation.velocity = vel
            localisation.angular_velocity = ang_vel
            time.sleep(0.1)




if __name__ == "__main__":
    detector = ObjectDetection()
    qr_detector = DetectQR()
    decision_maker = DecisionMaker()



    server = ServerCommunication(detector, decision_maker, qr_detector)
    server_queue = server.queue
    server.start_thread()

    localisation = Localisation()

    queue_thread = threading.Thread(target=retrieve_from_queue)
    queue_thread.start()
    
    
    localisation.root.mainloop()



