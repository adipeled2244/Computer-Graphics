# Students: 1) Noor Haj Dawood 2) Noy Shabo 3) Adi Peled

import tkinter as tk
import numpy as np
from tkinter import filedialog
import json
import math
from tkinter import messagebox
import random

colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "cyan", "magenta", "violet", "turquoise", "tan", "royal blue", "salmon", "plum", "orchid", "navy", "maroon", "lime", "lavender", "ivory", "indigo", "hot pink", "gold", "gray", "fuchsia", "forest green", "firebrick", "dark violet", "dark turquoise", "dark slate gray", "dark salmon", "dark red", "dark orchid", "dark olive green", "dark magenta", "dark khaki", "dark green", "dark cyan", "dark blue", "coral", "chocolate", "chartreuse", "cadet blue", "burlywood", "blue violet", "black", "beige", "azure", "aquamarine", "aqua", "antique white", "alice blue", "yellow green", "wheat", "violet red", "violet", "tomato", "thistle", "teal", "steel blue", "spring green", "snow", "slate gray", "sienna", "seashell", "sea green", "sandy brown", "salmon", "saddle brown", "rosy brown", "red", "purple", "powder blue", "plum", "pink", "peach puff", "papaya whip", "pale violet red", "pale turquoise", "pale green", "orchid", "orange red", "orange", "olive drab", "olive", "old lace", "navy", "navajo white", "moccasin", "misty rose", "mint cream", "midnight blue", "medium violet red", "medium turquoise", "medium spring green", "medium slate blue", "medium sea green", "medium purple", "medium orchid", "medium blue", "maroon", "magenta", "linen", "lime green", "light yellow", "light steel blue", "light slate gray", "light sky blue", "light salmon", "light pink", "light grey", "light green", "light goldenrod", "light cyan", "light coral", "light blue", "lavender blush", "lavender",]


class App():
    def __init__(self):
        self.root = None
        self.menubar = None
        self.canvas = None
        self.twoD_coords = None
        self.polygons = None
        self.threeD_coords = None
        self.mass_center = None
        self.current_projection = None
        self.current_transformation=None
        self.projection_params = None
     
    def validate_floats(self, input):
        """Validate float numbers"""
        if input == "":
            return True
        if input == "-":
            return True
        try:
            float(input)
            return True
        except ValueError:
            return False
        
        ######################################## show inputs functions ########################################
        
    def scaling_inputs(self):
        """Handle scaling inputs"""
        # popout window
        self.current_transformation = "scaling"
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Scaling")
        popout_window.geometry("300x200")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white")
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Enter the scaling factor", bg="white")
        popout_label.pack()
        # create a label for x scaling
        popout_label = tk.Label(popout_window, text="X", bg="white")
        popout_label.pack()
        # create an entry for x scaling
        x_popout_entry = tk.Entry(popout_window)
        # allow only float numbers
        x_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        x_popout_entry.pack()
        # create a label for y scaling
        popout_label = tk.Label(popout_window, text="Y", bg="white")
        popout_label.pack()
        # create an entry for y scaling
        y_popout_entry = tk.Entry(popout_window)
        # allow only numbers
        y_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        y_popout_entry.pack()
        # create a label for z scaling
        popout_label = tk.Label(popout_window, text="Z", bg="white")
        popout_label.pack()
        # create an entry for z scaling
        z_popout_entry = tk.Entry(popout_window)
        # allow only numbers
        z_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        z_popout_entry.pack()
        # handle the popout window button
        def handle_popout_button():
            # handel empty input
            x = 1 if x_popout_entry.get() == "" else x_popout_entry.get()
            y = 1 if y_popout_entry.get() == "" else y_popout_entry.get()
            z = 1 if z_popout_entry.get() == "" else z_popout_entry.get()
            if x == '-':
                x = -1
            if y == '-':
                y = -1
            if z == '-':
                z = -1
            self.submit(["transformation", float(x), float(y), float(z)])
            popout_window.destroy()
        # create a button for the popout window
        popout_button = tk.Button(popout_window, text="Submit", command=handle_popout_button)
        popout_button.pack()
    

    def oblique_inputs(self):
        """Handle oblique inputs"""
        # popout window
        self.current_projection = "oblique"  
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Oblique projection")
        popout_window.geometry("300x150")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white")
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Enter angle and scale", bg="white")
        popout_label.pack()
        # create a label for angle
        popout_label = tk.Label(popout_window, text="Angle", bg="white")
        popout_label.pack()
        # create an entry for angle
        angle_popout_entry = tk.Entry(popout_window)
        # allow only float numbers
        angle_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        angle_popout_entry.pack()
        # create a label for scale
        popout_label = tk.Label(popout_window, text="Scale", bg="white")
        popout_label.pack()
        # create an entry for scale
        scale_popout_entry = tk.Entry(popout_window)
        # allow only numbers
        scale_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        scale_popout_entry.pack()
        # handle the popout window button
        def handle_popout_button():
            # handel empty input
            angle = 45 if angle_popout_entry.get() == "" else angle_popout_entry.get()
            scale = 0.5 if scale_popout_entry.get() == "" else scale_popout_entry.get()
            self.submit(["projection",float(angle),float(scale) ])
            popout_window.destroy()
        # create a button for the popout window
        popout_button = tk.Button(popout_window, text="Submit", command=handle_popout_button)
        popout_button.pack()
    
    
    def orthographic_inputs(self):
        self.current_projection = "orthographic" 
        self.submit(["projection"])
        
    def perspective_inputs(self):
        """Handle oblique inputs"""
        # popout window
        self.current_projection = "perspective"  
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Perspective projection")
        popout_window.geometry("300x200")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white")
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Enter x y z", bg="white")
        popout_label.pack()
        # create a label for x
        popout_label = tk.Label(popout_window, text="x", bg="white")
        popout_label.pack()
        # create an entry for x
        x_popout_entry = tk.Entry(popout_window)
        # allow only float numbers
        x_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        x_popout_entry.pack()
       
        popout_label = tk.Label(popout_window, text="y", bg="white")
        popout_label.pack()
        # create an entry for y
        y_popout_entry = tk.Entry(popout_window)
        # allow only float numbers
        y_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        y_popout_entry.pack()
        
        popout_label = tk.Label(popout_window, text="z", bg="white")
        popout_label.pack()
        # create an entry for z
        z_popout_entry = tk.Entry(popout_window)
        # allow only float numbers
        z_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        z_popout_entry.pack()
        
        # handle the popout window button
        def handle_popout_button():
            # handel empty input
            x = 0 if x_popout_entry.get() == "" else x_popout_entry.get()
            y = 0 if y_popout_entry.get() == "" else y_popout_entry.get()
            z = 300 if z_popout_entry.get() == "" else z_popout_entry.get()
            self.submit(["projection", (float(x), float(y), float(z))])
            popout_window.destroy()
        # create a button for the popout window
        popout_button = tk.Button(popout_window, text="Submit", command=handle_popout_button)
        popout_button.pack() 

            
    def rotation_inputs(self):
        """Handle rotation inputs"""
        # popout window
        self.current_transformation = "rotation"
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Rotation")
        popout_window.geometry("300x150")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white")
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Enter the rotation angle and axis, ", bg="white")
        popout_label.pack()
        # create a label for x scaling
        popout_label = tk.Label(popout_window, text="Angle(degree)", bg="white")
        popout_label.pack()
        # create an entry for x scaling
        angle_popout_entry = tk.Entry(popout_window)
        # allow only float numbers
        angle_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        angle_popout_entry.pack()
        
         # create a button for the popout window
        def handle_popout_button(angle,axis):
            # handel empty input
            angle = 0 if angle_popout_entry.get() == "" or angle_popout_entry.get() == "-" else float(angle_popout_entry.get())
            angle = np.radians(angle)
            self.submit(["transformation",angle, axis])
            # popout_window.destroy()

        #axis buttons 
        x_popout_button = tk.Button(popout_window, text="X", command=lambda: handle_popout_button(angle_popout_entry.get(), "x"))
        x_popout_button.pack()
        y_popout_button = tk.Button(popout_window, text="Y", command=lambda: handle_popout_button(angle_popout_entry.get(), "y"))
        y_popout_button.pack()
        z_popout_button = tk.Button(popout_window, text="Z", command=lambda: handle_popout_button(angle_popout_entry.get(), "z"))
        z_popout_button.pack()
        
        


 ######################################## action functions ########################################

    def normal_vector(self, polygon):
        """Calculate the normal vector of a polygon"""
        p1 = self.threeD_coords[polygon[0]-1]
        p2 = self.threeD_coords[polygon[1]-1]
        p3 = self.threeD_coords[polygon[2]-1]
        # calculate two vectors of the polygon sides
        v1 = np.array([p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]])
        v2 = np.array([p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]])
        # calculate the normal vector by cross product
        return np.cross(v1, v2)
    
    def is_visible(self, polygon):
        """Check if a polygon is visible"""
        normal_vector = self.normal_vector(polygon)
        # get the COP according to the projection
        if self.current_projection == "perspective":
            cop = self.projection_params[0]
        else:
            cop = np.array([0, 0, -300])
        p1 = self.threeD_coords[polygon[0]-1]
        # calculate the vector from the COP to the first point of the polygon
        v = np.array([cop[0]-p1[0], cop[1]-p1[1], cop[2]-p1[2]])
        # result of dot product indicates if the polygon is visible
        return np.dot(normal_vector, v) > 0

    def painters_algorithm(self):
        """Sort the polygons by painters algorithm"""
        # sort polygons by their max z value
        self.polygons.sort(key=lambda polygon: max(self.threeD_coords[point-1][2] for point in polygon[:-1]), reverse=False)


    def project_coords(self, matrix):
        """ Get x, y from the 3D coordinates after the projection """
        points = np.dot(self.threeD_coords, matrix)
        self.twoD_coords = points[:, :2].tolist()

    # orthographic_projection- z zero 
    def orthographic_projection(self):
        """action of the orthographic projection"""
        matrix = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 1]])
    
        self.project_coords(matrix)


    #oblique_projection- cabinet
    def oblique_projection(self, angle_degrees, scale):
        """action of the oblique projection"""
        angle_radians = np.radians(angle_degrees)
        matrix = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [scale * np.cos(angle_radians), scale * np.sin(angle_radians), 0, 0],
                            [0, 0, 0, 1]])
        
        self.project_coords(matrix)

    # perspective_projection
    def perspective_projection(self, cop):
        """action of the perspective projection"""
        self.twoD_coords = []
        for point in self.threeD_coords:
            # calculate distance of copX, copY, copZ from the point
            distance = np.sqrt((point[0]-cop[0])**2 + (point[1]-cop[1])**2 + (point[2]-cop[2])**2)
            s = cop[2] / distance 
            matrix = np.array([[s, 0, 0, 0],
                                 [0, s, 0, 0],
                                 [0, 0, 0, 0],
                                 [0, 0, 0, 1]])
            vector = np.array([point[0], point[1], point[2], 1])
            point = np.dot(matrix, vector)
            self.twoD_coords.append([point[0], point[1]])

    # calculate the projection on the updated coordinates
    def recalculate_twoD_coords(self):
        """recalculate the coords after transformations"""
        if self.current_projection == "oblique":
            self.oblique_projection(self.projection_params[0], self.projection_params[1])
        elif self.current_projection == "perspective":
            self.perspective_projection(self.projection_params[0])
        elif self.current_projection == "orthographic":
            self.orthographic_projection()

    def submit(self, params):
        """Submit the transformation"""
        print(params)
        if params[0] == 'projection':
            self.projection_params = params[1:]
            
        elif params[0] == 'transformation':
            if self.current_transformation == "scaling":
                self.scaling(params[1:])
            elif self.current_transformation == "rotation":             
                self.rotation(params[1:])

        self.recalculate_twoD_coords()
        self.center()
        self.draw_data()

    
    def rotation(self,params):
        """Rotate the shape"""
        angle=params[0]
        axis=params[1]
        matrix = []
        sin = np.sin(angle)
        cos = np.cos(angle)
        if axis == "x":
            matrix = np.array([[1, 0, 0, 0],
                                [0, cos, -sin, 0],
                                [0, sin, cos, 0],
                                [0, 0, 0, 1]])
        elif axis == "y":
            matrix = np.array([[cos, 0, sin, 0],
                                [0, 1, 0, 0],
                                [-sin, 0, cos, 0],
                                [0, 0, 0, 1]])
        elif axis == "z":
            matrix = np.array([[cos, -sin, 0, 0],
                                [sin, cos, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
        self.threeD_coords = np.array(self.threeD_coords)
        self.threeD_coords = np.dot(self.threeD_coords, matrix)
        self.threeD_coords = self.threeD_coords.tolist()

    def translation(self,params):
        """Translate the shape"""
        translation_matrix = np.array([[1, 0, 0, params[0]],
                                [0, 1, 0, params[1]],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
        
        self.threeD_coords = np.array(self.threeD_coords)
        self.threeD_coords = np.dot(self.threeD_coords, translation_matrix)
        self.threeD_coords = self.threeD_coords.tolist()

    def translation2D(self,params):
        """Translate the shape"""
        for i in range(len(self.twoD_coords)):
            self.twoD_coords[i] = (
                self.twoD_coords[i][0] + params[0],
                self.twoD_coords[i][1] + params[1]
            )
        self.mass_center = self.calculate_mass_center()
        
    def scaling(self,params):
        """Scale the shape"""
        sx=params[0]
        sy=params[1]
        sz=params[2]
        
        matrix = np.array([[sx, 0,  0, 0],
                            [0, sy, 0, 0],
                            [0, 0, sz, 0],
                            [0, 0,  0, 1]])

        self.threeD_coords = np.array(self.threeD_coords)
        self.threeD_coords = np.dot(self.threeD_coords, matrix)
        self.threeD_coords = self.threeD_coords.tolist()
        
    def center(self):
        """Center the shape"""
        self.mass_center = self.calculate_mass_center()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x_translation = width/2 - self.mass_center[0]
        y_translation = height/2 - self.mass_center[1]
        self.translation2D([x_translation, y_translation])
        self.draw_data()

    def clear(self):
        """Clear the canvas"""
        self.canvas.delete("all")
        self.polygons = None
        self.current_projection = None
        self.current_transformation=None
        
        self.twoD_coords = []
        self.threeD_coords = []

        self.mass_center = [0, 0]
        self.disable_toolbar()

    def readFile(self, filename):
        """read the json file and return the data """
        try:
            coords = []
            polygons = []

            with open(filename, 'r') as file:
                lines = file.readlines()

                # Read coordinates
                coords_start = lines.index('#coords\n') + 1
                coords_end = lines.index('#polygons\n') -1
                for line in lines[coords_start:coords_end]:
                    coord_values = line.split(' ')[1].split(',')
                    # add 1 to coordinate vector for matrix multiplication
                    coord_values += [1]
                    coord_values = tuple(float(value) for value in coord_values)
                    coords.append(coord_values)
                self.threeD_coords = coords

                # Read polygons
                polygons_start = lines.index('#polygons\n')+1
                for line in lines[polygons_start:]:
                    polygon_vertices = line.split(" ")[1].split(',')
                    polygon_indices = [int(index) for index in polygon_vertices]
                    # add color to polygon
                    polygon_indices.append(colors[random.randint(0, len(colors)-1)])
                    polygons.append(polygon_indices)

                self.polygons = polygons
        except Exception:
            messagebox.showerror("Error", "TXT format is not valid.")
            return

    def calculate_mass_center(self):
        """calculate the mass center of the shape"""
        x_sum = 0
        y_sum = 0
        for coord in self.twoD_coords:
            x_sum += coord[0]
            y_sum += coord[1]

        return [0 if len(self.twoD_coords) == 0 else x_sum/len(self.twoD_coords), 0 if len(self.twoD_coords) == 0 else y_sum/len(self.twoD_coords)]
    

    def openHelpWindow(self):
        """handle help choice from the menu bar and open the help window"""
        # popout window
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Help")
        popout_window.geometry("600x200")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white",padx=10,pady=10)
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Hey, welcome !\n\nOptions:\n1- Upload New File- txt\n2- Choose transformation: Scale, Rotate , Fit, Center\n3- Projections- choose-Orthographic,Oblique,Perspective.  \n4- Clear window- press clear \n5- Exit- press exit\n\n\n\n* Empty transformation values have no effect.",  justify=tk.LEFT, bg="white" )
        popout_label.pack(side='left')

    def fitWindow(self):
        """fit the shape to the window"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x_min = min(self.threeD_coords, key=lambda coord: coord[0])[0]
        y_min = min(self.threeD_coords, key=lambda coord: coord[1])[1]
        z_min = min(self.threeD_coords, key=lambda coord: coord[2])[2]

        self.translation([-x_min, -y_min, -z_min])
        
        x_max = max(self.threeD_coords, key=lambda coord: coord[0])[0]
        y_max = max(self.threeD_coords, key=lambda coord: coord[1])[1]

        x_scale = width/(x_max)
        y_scale = height/(y_max)
        scale = 0.2*min(x_scale, y_scale)
        self.scaling([scale, scale, scale])
        self.recalculate_twoD_coords()

        self.center()
    
    def disable_toolbar(self):
        """disable the transformations button"""
        self.menubar.entryconfig('Transformations', state='disabled')
        self.menubar.entryconfig('Projections', state='disabled')


    def enable_toolbar(self):
        """enable the transformations button"""
        self.menubar.entryconfig('Transformations', state='normal')
        self.menubar.entryconfig('Projections', state='normal')
            
    def createMenu(self):
        """create the menu bar"""
        width = 800
        height = 600
        # root window
        root = tk.Tk()
        root.geometry(f'{width}x{height}')
        root.title('Menu Demo')

        # create a menubar
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)

        # create the file_menu
        file_menu = tk.Menu(
            self.menubar,
            tearoff=0
        )
        
        # add the File menu to the self.menubar
        self.menubar.add_cascade(
            label="File",
            menu=file_menu
        )
        file_menu.add_command(label='Upload New File',command=self.upload_file)

        transform_menu =tk. Menu(self.menubar)
        self.menubar.add_cascade(label="Transformations", menu=transform_menu)
        transform_menu.add_command(label='Scale',command=self.scaling_inputs)
        transform_menu.add_command(label='Rotate',command=self.rotation_inputs)
        transform_menu.add_command(label='Fit',command=self.fitWindow)
        transform_menu.add_command(label='Center',command=self.center)

        self.menubar.entryconfig('Transformations', state='disabled')

        projection_menu =tk. Menu(self.menubar)
        self.menubar.add_cascade(label="Projections", menu=projection_menu)
        projection_menu.add_command(label='Orthographic',command=self.orthographic_inputs)
        projection_menu.add_command(label='Oblique',command=self.oblique_inputs)
        projection_menu.add_command(label='Perspective ',command=self.perspective_inputs)

        self.menubar.entryconfig('Projections', state='disabled')
        
        self.menubar.add_command(label="Clear", command=self.clear)
        self.menubar.add_command(label="Exit", command=root.destroy)
        self.menubar.add_command(label="Help", command=self.openHelpWindow)

        self.canvas = tk.Canvas(
            root,
            width=width,
            height=height,
            bg='white'
        )
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.root = root
        return root

    def draw_data(self):
        """draw the shape on the canvas"""
        self.canvas.delete("all")
        if self.current_projection == "perspective":
            self.painters_algorithm()
        for polygon in self.polygons:
            if self.current_projection == "perspective" and not self.is_visible(polygon):
                continue
            coordinates = [self.twoD_coords[coordinate-1] for coordinate in polygon[:-1] ]
            fill = polygon[-1]
            self.canvas.create_polygon(coordinates, outline='black', fill=fill)
        return

    def update_data(self, file_path):
        """update the data from the file"""
        if file_path == '':
            return
        self.readFile(file_path)
        self.current_projection = "perspective"
        self.projection_params = [(0, 0, 300)]
        self.perspective_projection((0, 0, 300))
        self.fitWindow()
        self.draw_data()
        self.enable_toolbar()

    def upload_file(self):
        """upload a json file"""
        # Open a file dialog window
        file_path = filedialog.askopenfilename(initialdir="/",title="select a file",filetypes=(("txt files","*.txt"),("all files",  "*.*")))
        self.update_data(file_path)


if __name__ == "__main__":
    app=App()
    root=app.createMenu()
    root.mainloop()