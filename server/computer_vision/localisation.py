import math
import tkinter as tk
import threading

class Localisation:

    def __init__(self):
        self.position = (0,0)
        self.orientation = -math.pi # in tkinter 180 is left. in my program -90 is left.
        self.top_left_boundary = (-1,1)
        self.top_right_boundary = (1,1)
        self.bottom_left_boundary = (-1,-1)
        self.bottom_right_boundary = (1,-1)
        self.time_interval = 0.1
        self.velocity = 0
        self.angular_velocity = 0
        self.robot_size = 20
        self.canvas_width = 500
        self.canvas_height = 500
        self.movement_const = 10

        self.border_width = self.canvas_width / 10

        

        self.start_gui()



    def start_gui(self):
        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title("Dead Reckoning")

        # Create a canvas to draw on
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.canvas.create_rectangle(self.border_width, self.border_width, self.canvas_width - self.border_width, self.canvas_width - self.border_width, fill="green")

        corner_radius = 10
        corner_coordinates = [self.top_left_boundary, self.top_right_boundary, self.bottom_left_boundary, self.bottom_right_boundary]
        for coord in corner_coordinates:

            if coord[0] == 1:
                center_x = self.canvas_width - self.border_width
            else:
                center_x = self.border_width

            if coord[1] == 1:
                center_y = self.canvas_width - self.border_width
            else:
                center_y = self.border_width

            self.canvas.create_oval(center_x - corner_radius, center_y - corner_radius, center_x + corner_radius, center_y + corner_radius, outline="black", fill="red")


        # Start a separate thread to update the position
        thread = threading.Thread(target=self.update)
        thread.daemon = True
        thread.start()


        

            
    
    def update(self):
        # Update position
        delta_x = (self.velocity * self.movement_const) * math.cos(self.orientation) * self.time_interval
        delta_y = (self.velocity * self.movement_const) * math.sin(self.orientation) * self.time_interval
        self.position = (self.position[0] + delta_x, self.position[1] + delta_y)

        # Update orientation
        self.orientation -= self.angular_velocity * self.time_interval

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


        # Draw the robot
        self.canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3, fill="blue", tags="robot", outline="black")




        self.root.after(int(1000 * self.time_interval), self.update)

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