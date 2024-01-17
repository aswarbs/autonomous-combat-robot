
import math 
import random

class DecisionTree():

    # all the states need to be in here

    def __init__(self, horizontal_midpoint, vertical_midpoint, area_threshold):
        self.player_midpoint_x = horizontal_midpoint
        self.player_midpoint_y = vertical_midpoint
        self.area_threshold = area_threshold
        self.state = "INITIAL"
        self.MOVEMENT_CONST = 10

    def run(self, opponent_information, qr_information, position, orientation, area):

        self.position = position

        if(opponent_information is not None and len(opponent_information) > 0):
            

            self.state="FOLLOW"

            if((orientation < -135 and orientation > -180) or (orientation > 135 and orientation < 180)):
                # facing the back of the cube, attack
                print("ATTACK")
                

            if(orientation > -45 and orientation < 45):
                # faccing the front of the cube, defend
                print("DEFEND")
                self.state ="FLEE"

            if(area < self.area_threshold):
                self.state = "RANDOM_WALK"

            
        else:
            self.state="RANDOM_WALK"

        if self.state == "RANDOM_WALK":
            rotations = self.random_walk()
            print(f"sending {[(self.MOVEMENT_CONST, x) for x in rotations]}")
            return [(self.MOVEMENT_CONST, x) for x in rotations], self.state
        elif self.state =="FOLLOW":
            rotations = self.follow()
            print(f"sending {[(self.MOVEMENT_CONST, x) for x in rotations]}")
            return [(self.MOVEMENT_CONST, x) for x in rotations], self.state
        elif self.state == "FLEE":
            # follow but move
            rotations = self.follow()
            print(f"sending {[(-self.MOVEMENT_CONST, x) for x in rotations]}")
            return [(-self.MOVEMENT_CONST, x) for x in rotations], self.state

        else:
            print(f"state is not in valid states: {self.state}")

    def follow(self):
        # from self.position = the position of the robot on the screen, 
        # work out the angle to turn to go towards the robot

        cube_midpoint_x = (self.position[0] + self.position[2]) / 2
        cube_midpoint_y = (self.position[1] + self.position[3]) / 2 

        angle_rad = math.atan2(cube_midpoint_x - self.player_midpoint_x, cube_midpoint_y - self.player_midpoint_y)
        angle_deg = math.degrees(angle_rad)

        print(f"player midpoint: {self.player_midpoint_x, self.player_midpoint_y} cube midpoint: {cube_midpoint_x, cube_midpoint_y}, angle: {angle_deg}")

        rotations = [angle_deg/10]

        return rotations

    def random_walk(self):

        max_angle_change = 30.0

        # Generate a random angle change for rotation
        angle_change = random.uniform(-max_angle_change, max_angle_change)

        rotations = [angle_change]

        # The robot always will move forward in random walk
        # The rotation is the random element
        return rotations
    


        