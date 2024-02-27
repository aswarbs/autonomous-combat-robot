
import math 
import random

# the movement is a constant, either -10 or 10
# the rotation is normalised between -1 and 1

class DecisionTree():

    def __init__(self, horizontal_midpoint, vertical_midpoint, area_threshold):
        self.player_midpoint_x = horizontal_midpoint
        self.player_midpoint_y = vertical_midpoint
        self.area_threshold = area_threshold
        self.state = "INITIAL"
        self.MOVEMENT_CONST = 1

    def run(self, opponent_information, qr_information, position, orientation, area):

        self.position = position

        if(opponent_information is not None and len(opponent_information) > 0 and orientation is not None):
            

            self.state="FOLLOW"

            if((orientation < -135 and orientation > -180) or (orientation > 135 and orientation < 180)):
                # facing the back of the cube, attack
                print("ATTACK")
                

            if(orientation > -45 and orientation < 45):
                # facing the front of the cube, defend
                print("DEFEND")
                self.state ="FLEE"

            if(area < self.area_threshold):
                self.state = "RANDOM_WALK"

            
        else:
            self.state="RANDOM_WALK"

        if self.state == "RANDOM_WALK":
            rotations = self.random_walk()
            movement = self.MOVEMENT_CONST
            
        elif self.state =="FOLLOW":
            rotations = self.follow()
            movement = self.MOVEMENT_CONST
            print(f"sending {[(self.MOVEMENT_CONST, x) for x in rotations]}")
        elif self.state == "FLEE":
            # follow but move
            rotations = self.follow()
            movement = -self.MOVEMENT_CONST
            print(f"sending {[(-self.MOVEMENT_CONST, x) for x in rotations]}")

        else:
            print(f"state is not in valid states: {self.state}")
            return None
        
    
        for x in rotations:
            print(movement, x)
            
        return [(movement, x) for x in rotations], self.state

    def follow(self):
        # from self.position = the position of the robot on the screen, 
        # work out the angle to turn to go towards the robot

        cube_midpoint_x = (self.position[0] + self.position[2]) / 2
        cube_midpoint_y = (self.position[1] + self.position[3]) / 2 

        angle_rad = math.atan2(cube_midpoint_x - self.player_midpoint_x, cube_midpoint_y - self.player_midpoint_y)
        angle_normalized = angle_rad / math.pi

        rotations = [angle_normalized]

        return rotations

    def random_walk(self):

        # Generate a random angle change for rotation
        angle_change = random.uniform(-1, 1)

        rotations = [angle_change]

        # The robot always will move forward in random walk
        # The rotation is the random element
        return rotations
    


        