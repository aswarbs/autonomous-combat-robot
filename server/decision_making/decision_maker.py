

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

    def run(self, image_information):
        """
        Run the decision making algorithm.
        image_information: Useful information about the image, retrieved from computer vision model.
        robot_movements: Array containing the decided robot movements.
        """

        position = image_information[0]["position"]
        orientation = image_information[0]["orientation"]
        bounding_box_area = image_information[0]["bounding_box_area"]

        print(f"position: {position}, orientation: {orientation}, area: {bounding_box_area}")

        movement = random.randint(-20,20)
        rotation = random.randint(-80,80)

        robot_movements = [movement, rotation]

        return robot_movements