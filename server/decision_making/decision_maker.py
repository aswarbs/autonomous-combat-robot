

import random


class DecisionMaker():
    """
    Decision making class. This will be passed information about the current image and calculate the next move for the robot to take.
    """

    def __init__(self):
        """
        Initialise the decision making model.
        """
        pass

    def run(self, opponent_information, qr_information):
        """
        Run the decision making algorithm.
        opponent_information: Useful information about the image, retrieved from computer vision model.
        robot_movements: Array containing the decided robot movements.
        """

        self.position = -1
        self.orientation = -1
        self.bounding_box_area = -1

        # DETECT_RUBRIK INFORMATION CONTAINS A 0 AS FOR NOW WE ARE JUST EVALUATING THE FIRST (ONLY) CUBE

        if(len(opponent_information) > 0):
            self.position = opponent_information[0]["position"] 
            self.orientation = opponent_information[0]["orientation"]
            self.bounding_box_area = opponent_information[0]["bounding_box_area"]

        # QR INFORMATION 
        self.qr_information = qr_information

        print(f"position: {self.position}, orientation: {self.orientation}, area: {self.bounding_box_area}, qr info: {self.qr_information}")

        movement = random.randint(-20,20)
        rotation = random.randint(-80,80)

        robot_movements = [movement, rotation]

        return robot_movements