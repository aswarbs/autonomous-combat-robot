

import random


class DecisionMaker():
    """
    Decision making class. This will be passed information about the current image and calculate the next move for the robot to take.
    """

    

    def __init__(self):
        """
        Initialise the decision making model.
        """

        self.MOVEMENT_CONST = 10
        self.state = "RANDOM_WALK"

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
        else:
            self.state="RANDOM_WALK"

        # QR INFORMATION 
        self.qr_information = qr_information

        print(f"position: {self.position}, orientation: {self.orientation}, area: {self.bounding_box_area}, qr info: {self.qr_information}")

        if(self.state == "RANDOM_WALK"):
            rotations = self.random_walk()
            print(f"sending {[(self.MOVEMENT_CONST, x) for x in rotations]}")
            return [(self.MOVEMENT_CONST, x) for x in rotations]
        else:
            return (self.MOVEMENT_CONST,0)
    

    def random_walk(self):

        max_angle_change = 30.0

        # Generate a random angle change for rotation
        angle_change = random.uniform(-max_angle_change, max_angle_change)

        rotations = [angle_change]

        # The robot always will move forward in random walk
        # The rotation is the random element
        return rotations
    


        