
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
        self.boundary_threshold = 35
        self.boundary_threshold_alternate = 65
        self.boundary_corners = boundary_corners
        self.localisation = localisation

    def calculate_boundary_distance(self):
        # return the distance
        # return the orientation e.g. LEFT, RIGHT, UP, DOWN

        lower_bound, upper_bound = self.boundary_corners
        x, y = self.player_position

        possible_distances = [[x - lower_bound, "LEFT"], [upper_bound - x, "RIGHT"], [y - lower_bound, "UP"], [upper_bound - y, "DOWN"]]

        # have different boundaries for left, right, vs up, down?

        counter = 0

        if possible_distances[0][0] < self.boundary_threshold:
            counter +=1
        if possible_distances[1][0] < self.boundary_threshold:
            counter +=1
        if possible_distances[2][0] < self.boundary_threshold_alternate:
            counter +=1
        if possible_distances[3][0] < self.boundary_threshold_alternate:
            counter +=1



        # Sort the list based on distances
        possible_distances.sort()

        if counter > 1:
            print("multiple boundaries")
            return True, possible_distances[0]

        return False, possible_distances[0]




    def run(self, opponent_information, qr_information, position, orientation, area, player_position, player_orientation):

        self.position = position
        self.player_position = player_position
        attack = False

        print("RUNNING DECISION TREE")

        multiple_boundaries, closest_boundary = self.calculate_boundary_distance()

        if multiple_boundaries:
            return [(-0.25, -1)], "BOUNDARY", False

        self.state = "RANDOM_WALK"

        print(f"opponent info: {opponent_information}, orientation: {orientation}")

        self.localisation.print_message("")

        
        if closest_boundary[0] < self.boundary_threshold:
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
            movement, rotations = self.boundary_avoidance(player_position, player_orientation, closest_boundary)
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
    
    def boundary_avoidance(self, position, orientation, closest_boundary):
        print(f"position: {position}. orientation: {orientation}. closest boundary: {closest_boundary}")

        """
    
        if the robot is facing the wall: MOVE BACKWARDS
        if the robot is facing away from the wall: MOVE FORWARDS
        if the wall is on the robot's left: MOVE FORWARDS SLOWLY AND ROTATE RIGHT
        if the wall is on the robot's right: MOVE FORWARDS SLOWLY AND ROTATE LEFT


        """

        print(f"closest boundary: {closest_boundary[1]}")

        if closest_boundary[1] not in ["UP", "DOWN", "LEFT", "RIGHT"]:

            print(f"not in valid bounds")
            return

        if closest_boundary[1] == "UP":
            wall_orientation = 0 # /360
            forward = [7 * math.pi/4, math.pi/4]
            left = [math.pi/4, 3 * math.pi/4]
            right = [5 * math.pi / 4, 7 * math.pi / 4]
            back = [3 * math.pi / 4, 5 * math.pi/4]
        if closest_boundary[1] == "RIGHT":
            wall_orientation = math.pi/2
            forward = [math.pi / 4, 3 * math.pi/4]
            left = [3 * math.pi / 4, 5 * math.pi / 4]
            right = [7 * math.pi / 4, math.pi / 4] 
            back = [5 * math.pi/4, 7 * math.pi/4]
        if closest_boundary[1] == "DOWN":
            wall_orientation = math.pi
            forward = [3 * math.pi / 4, 5 * math.pi/4]
            left = [5 * math.pi / 4, 7 * math.pi / 4]
            right = [math.pi / 4, 3 * math.pi / 4]
            back = [7 * math.pi/4, math.pi/4]
        if(closest_boundary[1] == "LEFT"):
            wall_orientation = 3 * math.pi / 2
            forward = [5 * math.pi/4, 7 * math.pi/4]
            left = [7 * math.pi / 4, math.pi / 4]
            right = [3 * math.pi / 4, 5 * math.pi / 4]
            back = [math.pi / 4, 3 * math.pi / 4]

        print(f"orientation: {math.degrees(orientation)} degrees")


        directions = [forward, left, right, back]

        chosen_num = 0

        for x in range(len(directions)):
            if directions[x][0] > directions[x][1]:
                # going over 2pi
                if(orientation >= directions[x][0] or orientation <= directions[x][1]):
                    chosen_num = x
            else:
                if(orientation >= directions[x][0] and orientation <= directions[x][1]):
                    chosen_num = x
                    

        if chosen_num == 0:
            print("DIRECTION IS FORWARD")
            # direction is forward
            return -1, [0]
        if chosen_num == 1:
            print("DIRECTION IS LEFT")
            # direction is left
            return 0.2, [1]
        if chosen_num == 2:
            print("DIRECTION IS RIGHT")
            # direction is right
            return 0.2, [-1]
        
        print("DIRECTION IS BACKWARDS")
        return 1, [0]

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
    


        