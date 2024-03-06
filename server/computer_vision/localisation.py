import math
import tkinter as tk

class Localisation:

    def __init__(self):
        self.position = (0,0)
        self.orientation = 0 

        self.arena_width = 250
        self.arena_height = 250
        self.qr_width = 30

        self.arena_offset = 0 # arena is shifted 25 to the left

        self.top_left_boundary = (self.arena_offset,self.arena_height + self.arena_offset)
        self.top_right_boundary = (self.arena_width + self.arena_offset, self.arena_height + self.arena_offset)
        self.bottom_left_boundary = (self.arena_offset,self.arena_offset)
        self.bottom_right_boundary = (self.arena_width + self.arena_offset,self.arena_offset)

        self.top_left_facing_south_position = (self.top_left_boundary[0] + (self.qr_width / 2), self.top_left_boundary[1])
        self.top_left_facing_east_position = (self.top_left_boundary[0], self.top_left_boundary[1] - (self.qr_width / 2))

        self.top_right_facing_south_position = (self.top_right_boundary[0] - (self.qr_width / 2), self.top_right_boundary[1])
        self.top_right_facing_west_position = (self.top_right_boundary[0], self.top_right_boundary[1] - (self.qr_width / 2))

        self.bottom_left_facing_north_position = (self.bottom_left_boundary[0] + (self.qr_width / 2), self.bottom_left_boundary[1])
        self.bottom_left_facing_east_position = (self.bottom_left_boundary[0], self.bottom_left_boundary[1] + (self.qr_width / 2))

        self.bottom_right_facing_north_position = (self.bottom_right_boundary[0] - (self.qr_width / 2), self.bottom_right_boundary[1])
        self.bottom_right_facing_west_position = (self.bottom_right_boundary[0], self.bottom_right_boundary[1] + (self.qr_width / 2))

        print(f"boundaries: {self.top_left_boundary}, {self.top_right_boundary}, {self.bottom_left_boundary}, {self.bottom_right_boundary}")

        print(f"qrs: {self.top_left_facing_south_position}, {self.top_left_facing_east_position}, {self.top_right_facing_south_position}, {self.top_right_facing_west_position}, {self.bottom_left_facing_north_position}, {self.bottom_left_facing_east_position}, {self.bottom_right_facing_north_position}, {self.bottom_right_facing_west_position}")

        self.time_difference = 0
        self.velocity = 0
        self.angular_velocity = 0
        self.robot_size = 9
        self.border_width = 10

        



        self.canvas_width = self.arena_width + self.border_width
        self.canvas_height = self.arena_height + self.border_width
        
        self.opponent_pos = (self.border_width + 180,self.border_width + 100)

        


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


            
        
    def update(self):
            
            self.orientation -= self.angular_velocity * self.time_difference


            # Update position
            delta_x = self.velocity * math.cos(self.orientation)
            delta_y = self.velocity * math.sin(self.orientation)

            #print(f"position: {self.position}")
            
            self.position = (self.position[0] + delta_x, self.position[1] + delta_y)

            # Update orientation
           

            # Map position to screen coordinates
            screen_x = self.canvas_width / 2 + self.position[0] 
            screen_y = self.canvas_height / 2 - self.position[1] 

            # Clear previous drawing
            self.canvas.delete("robot")

            x0 = screen_x + self.robot_size/2 * math.cos(self.orientation) - self.robot_size/2 * math.sin(self.orientation)
            y0 = screen_y - self.robot_size/2 * math.sin(self.orientation) - self.robot_size/2 * math.cos(self.orientation)
            x1 = screen_x - self.robot_size/2 * math.cos(self.orientation) - self.robot_size/2 * math.sin(self.orientation)
            y1 = screen_y + self.robot_size/2 * math.sin(self.orientation) - self.robot_size/2 * math.cos(self.orientation)
            x2 = screen_x - self.robot_size/2 * math.cos(self.orientation) + self.robot_size/2 * math.sin(self.orientation)
            y2 = screen_y + self.robot_size/2 * math.sin(self.orientation) + self.robot_size/2 * math.cos(self.orientation)
            x3 = screen_x + self.robot_size/2 * math.cos(self.orientation) + self.robot_size/2 * math.sin(self.orientation)
            y3 = screen_y - self.robot_size/2 * math.sin(self.orientation) + self.robot_size/2 * math.cos(self.orientation)

            #print(f"{x0} {y0}, {x1} {y1}, {x2} {y2}, {x3} {y3}")


            # Draw the robot
            self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill="blue", tags="robot", outline="black")

        
            self.root.after(100,self.update)


        
    def get_position(self):
        return self.position

    def get_orientation(self):
        return self.orientation

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_angular_velocity(self, angular_velocity):
        self.angular_velocity = angular_velocity


if __name__ == "__main__":
    loc = Localisation()
    loc.root.mainloop()