

import random
import math
import os
from decision_making.decision_tree import DecisionTree


# attack state is follow
# defend state is run away


class DecisionMaker():

    def __init__(self, boundary_corners, localisation):
        """
        Initialise the decision making model.
        """
        self.IMAGE_WIDTH = 397
        self.IMAGE_HEIGHT = 376
        self.HORIZONTAL_MIDPOINT = int(self.IMAGE_WIDTH / 2)
        self.VERTICAL_MIDPOINT = 0
        self.AREA_THRESHOLD = 1500
        self.BOUNDARY_THRESHOLD = 50
        self.boundary_corners = boundary_corners
        self.localisation = localisation
        

        self.state = "RANDOM_WALK"

        self.model = DecisionTree(self.HORIZONTAL_MIDPOINT, self.VERTICAL_MIDPOINT, self.AREA_THRESHOLD, self. BOUNDARY_THRESHOLD, self.boundary_corners, self.localisation)

    def run(self, opponent_information, qr_information, player_position):
        """
        Run the decision making algorithm.
        opponent_information: Useful information about the image, retrieved from computer vision model.
        robot_movements: Array containing the decided robot movements.
        """

        self.position = -1
        self.orientation = -1
        self.bounding_box_area = -1
        self.qr_information = qr_information

        if opponent_information is not None and len(opponent_information) > 0:       
            self.position = opponent_information[0]["position"] 
            self.orientation = opponent_information[0]["orientation"]
            self.bounding_box_area = opponent_information[0]["bounding_box_area"]


        

        return self.model.run(opponent_information, qr_information, self.position, self.orientation, self.bounding_box_area, player_position)
        
    