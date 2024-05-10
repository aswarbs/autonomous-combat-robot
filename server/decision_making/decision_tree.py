
import math 
import random

# the movement is a constant, either -10 or 10
# the rotation is normalised between -1 and 1

class DecisionTree():

    def __init__(self, horizontal_midpoint, vertical_midpoint, area_threshold, boundary_threshold, boundary_corners, localisation):
        self.player_midpoint_x = horizontal_midpoint
        self.player_midpoint_y = vertical_midpoint
        self.area_threshold = area_threshold
        self.state = "INITIAL"
        self.MOVEMENT_CONST = 1
        self.boundary_threshold = boundary_threshold
        self.boundary_corners = boundary_corners
        self.localisation = localisation

    def calculate_boundary_distance(self):
        # return the distance
        # return the orientation e.g. LEFT, RIGHT, UP, DOWN

        lower_bound, upper_bound = self.boundary_corners
        x, y = self.player_position

        possible_distances = [[x - lower_bound, "LEFT"], [upper_bound - x, "RIGHT"], [y - lower_bound, "UP"], [upper_bound - y, "DOWN"]]

        # Find and return the element with the lowest first element
        result = min(possible_distances, key=lambda item: item[0])
        return result




    def run(self, opponent_information, qr_information, position, orientation, area, player_position):

        self.position = position
        self.player_position = player_position
        attack = False

        print("RUNNING DECISION TREE")

        closest_boundary = self.calculate_boundary_distance()

        self.state = "RANDOM_WALK"

        print(f"opponent info: {opponent_information}, orientation: {orientation}")

        
        if closest_boundary[0] < self.boundary_threshold:
            print(f"\n\nNEAR BOUNDARY ON [{closest_boundary}]")
            self.localisation.print_message(f"CLOSE TO {closest_boundary[1]}: {round(closest_boundary[0],2)}m AWAY")
            self.state = "BOUNDARY"


        elif(opponent_information is not None and len(opponent_information) > 0 and orientation is not None):
            

            self.state="FOLLOW"

        

            if((orientation < -135 and orientation > -180) or (orientation > 135 and orientation < 180)):
                # facing the back of the cube, attack
                print("ATTACK")
                attack = True
                

            if(orientation > -45 and orientation < 45):
                # facing the front of the cube, defend
                print("DEFEND")
                self.state ="FLEE"

            if(area < self.area_threshold):
                self.state = "RANDOM_WALK"


        
        if self.state == "BOUNDARY":
            movement, rotations = self.boundary_avoidance(player_position, closest_boundary)
        elif self.state == "RANDOM_WALK":
            rotations = self.random_walk()
            movement = random.uniform(0, self.MOVEMENT_CONST)
            
        elif self.state =="FOLLOW":
            rotations = self.follow()
            movement = random.uniform(0, self.MOVEMENT_CONST)
        elif self.state == "FLEE":
            # follow but move
            rotations = self.follow()
            movement = random.uniform(-self.MOVEMENT_CONST, 0)

        else:
            print(f"state is not in valid states: {self.state}")
            return None
        
    
        for x in rotations:
            print(movement, x)
            
        return [(movement, x) for x in rotations], self.state, attack
    
    def boundary_avoidance(self, position, closest_boundary):
        print(f"position: {position}. closest boundary: {closest_boundary}")
        return -1, [0]

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
    


        