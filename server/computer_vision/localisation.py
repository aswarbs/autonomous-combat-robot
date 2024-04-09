import math
import tkinter as tk
import sympy as sym

class Localisation:

    def __init__(self):

        
        self.orientation = math.pi/2

        self.text = ""

        self.arena_width = 250
        self.arena_height = 250
        self.qr_width = 30

        self.position = (int(self.arena_width / 2),int(self.arena_height / 2))

        self.lower_bound_x = 0
        self.lower_bound_y = 0
        self.upper_bound_x = self.arena_width
        self.upper_bound_y = self.arena_height

        self.arena_offset = 0 # arena is shifted 25 to the left

        self.top_left_boundary = (self.arena_offset,self.arena_height + self.arena_offset)
        self.top_right_boundary = (self.arena_width + self.arena_offset, self.arena_height + self.arena_offset)
        self.bottom_left_boundary = (self.arena_offset,self.arena_offset)
        self.bottom_right_boundary = (self.arena_width + self.arena_offset,self.arena_offset)

        self.boundary_corners = [self.lower_bound_x, self.upper_bound_x]

        self.top_left_facing_south_position = (self.top_left_boundary[0] + (self.qr_width / 2), self.top_left_boundary[1])
        self.top_left_facing_east_position = (self.top_left_boundary[0], self.top_left_boundary[1] - (self.qr_width / 2))

        self.top_right_facing_south_position = (self.top_right_boundary[0] - (self.qr_width / 2), self.top_right_boundary[1])
        self.top_right_facing_west_position = (self.top_right_boundary[0], self.top_right_boundary[1] - (self.qr_width / 2))

        self.bottom_left_facing_north_position = (self.bottom_left_boundary[0] + (self.qr_width / 2), self.bottom_left_boundary[1])
        self.bottom_left_facing_east_position = (self.bottom_left_boundary[0], self.bottom_left_boundary[1] + (self.qr_width / 2))

        self.bottom_right_facing_north_position = (self.bottom_right_boundary[0] - (self.qr_width / 2), self.bottom_right_boundary[1])
        self.bottom_right_facing_west_position = (self.bottom_right_boundary[0], self.bottom_right_boundary[1] + (self.qr_width / 2))

        self.time_difference = 0
        self.velocity = 0
        self.angular_velocity = 0
        self.robot_size = 9
        self.border_width = 10

        self.frame_rate = 0.1

        self.labels_to_coordinates = {
            "top_left_facing_south": self.top_left_facing_south_position,
            "top_left_facing_east": self.top_left_facing_east_position,
            "top_right_facing_south": self.top_right_facing_south_position,
            "top_right_facing_west": self.top_right_facing_west_position,
            "bottom_left_facing_north": self.bottom_left_facing_north_position,
            "bottom_left_facing_east":  self.bottom_left_facing_east_position,
            "bottom_right_facing_north": self.bottom_right_facing_north_position,
            "bottom_right_facing_west": self.bottom_right_facing_west_position
        }


        



        self.canvas_width = self.arena_width + self.border_width
        self.canvas_height = self.arena_height + self.border_width
        
        self.opponent_pos = (self.border_width + 100,self.border_width + (self.arena_height -180))

        


        self.start_gui()

        self.update()



    def start_gui(self):
        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title("Dead Reckoning")

        # Create a canvas to draw on
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.canvas.create_rectangle(self.border_width, self.border_width, self.canvas_width - self.border_width, self.canvas_width - self.border_width, fill="green")

        corner_radius = 10
        coord = [self.top_left_boundary, self.top_right_boundary, self.bottom_left_boundary, self.bottom_right_boundary]
        borders = [(1, -1/2), (0, -1/2), (1, 1), (0, 1)]
        for x in range(len(coord)):
            self.canvas.create_oval((coord[x][0] - corner_radius) + (self.border_width * borders[x][0]) , (coord[x][1] - corner_radius) + (self.border_width * borders[x][1]), (coord[x][0] + corner_radius) + (self.border_width * borders[x][0]), (coord[x][1] + corner_radius) + (self.border_width * borders[x][1]), outline="black", fill="red")

        self.canvas.create_oval(self.opponent_pos, self.opponent_pos[0] + 10, self.opponent_pos[1] + 10, outline="black", fill="yellow")

        self.text_id = self.canvas.create_text(130, 50, text=self.text, fill="red", font=('Helvetica', 10, 'bold'))



    

    def find_orientation(self, labels_to_distances):

        pos = []
        for k in labels_to_distances:
            pos.append(self.labels_to_coordinates[k])


        midpoint_x = pos[0][0] + pos[1][0] / 2
        midpoint_y = pos[0][1] + pos[1][1] / 2

        # find the angle between position and pos
        angle = math.atan2(midpoint_y-self.position[1], midpoint_x-self.position[0]) + math.pi
        #adjusted_angle = (-angle) % (2 * math.pi)  # Ensure the angle is within 0 to 2π
        #if angle < 0:
        #    angle += math.pi
        self.orientation = -angle

    def print_message(self, text):
        self.text = text
        

    def update(self):
            
            self.orientation += self.angular_velocity


            # Update position
            delta_x = self.velocity * math.cos(self.orientation)
            delta_y = self.velocity * math.sin(self.orientation)

            self.position = (self.position[0] - delta_x, self.position[1] - delta_y)

            screen_x = self.position[0] + delta_x + self.border_width
            screen_y = self.position[1] + delta_y + self.border_width

            # Update orientation
           

            # Clear previous drawing
            self.canvas.delete("robot")

            x0 = screen_x + self.robot_size/2 * math.cos(-self.orientation) - self.robot_size/2 * math.sin(-self.orientation)
            y0 = screen_y - self.robot_size/2 * math.sin(-self.orientation) - self.robot_size/2 * math.cos(-self.orientation)
            x1 = screen_x - self.robot_size/2 * math.cos(-self.orientation) - self.robot_size/2 * math.sin(-self.orientation)
            y1 = screen_y + self.robot_size/2 * math.sin(-self.orientation) - self.robot_size/2 * math.cos(-self.orientation)
            x2 = screen_x - self.robot_size/2 * math.cos(-self.orientation) + self.robot_size/2 * math.sin(-self.orientation)
            y2 = screen_y + self.robot_size/2 * math.sin(-self.orientation) + self.robot_size/2 * math.cos(-self.orientation)
            x3 = screen_x + self.robot_size/2 * math.cos(-self.orientation) + self.robot_size/2 * math.sin(-self.orientation)
            y3 = screen_y - self.robot_size/2 * math.sin(-self.orientation) + self.robot_size/2 * math.cos(-self.orientation)



            # Draw the robot
            self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill="blue", tags="robot", outline="black")

            
            self.canvas.itemconfig(self.text_id, text=self.text)

        
            self.root.after(100,self.update)


        
    def get_position(self):
        return self.position

    def get_orientation(self):
        return self.orientation

    def set_velocity(self, velocity):
        self.velocity = velocity * self.frame_rate

    def set_angular_velocity(self, angular_velocity):
        self.angular_velocity = angular_velocity * self.frame_rate


if __name__ == "__main__":
    loc = Localisation()
    loc.root.mainloop()