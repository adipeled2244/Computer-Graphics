# Students: 1) Noor Haj Dawood 2) Noy Shabo 3) Adi Peled

import tkinter as tk
import numpy as np
from tkinter import filedialog
import json
import math
from tkinter import messagebox


class App():
    def __init__(self):
        self.root = None
        self.menubar = None
        self.canvas = None
        self.points = None
        self.mass_center = None
        self.lines = None
        self.circles = None
        self.curves=None
        self.current_transformation=None
        self.translate_start_point = [0, 0]
        self.translate_end_point = [0, 0]
        
    def draw_lines(self):
        """Draw lines on the canvas"""
        for line in self.lines:
            x1, y1 = self.points[line[0]][0], self.points[line[0]][1]
            x2, y2 = self.points[line[1]][0], self.points[line[1]][1]
            self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2)

    def draw_circles(self):
        """Draw circles on the canvas"""
        for circle in self.circles:
            x, y = self.points[circle[0]][0], self.points[circle[0]][1]
            r = circle[1]          
            self.canvas.create_oval(x-r, y-r, x+r, y+r, outline='red', width=2)

    def bezier_curve(self, points, n=100):
        """Calculate bezier curve points"""
        control_points = np.array(points)
        bernstein_matrix = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
        t = np.linspace(0, 1, n)
        t_matrix = np.array([t**3, t**2, t, np.ones(n)])
        curve = np.dot(np.dot(t_matrix.T, bernstein_matrix), control_points)
        return curve

    def draw_bezier_curves(self):
        """Draw bezier curves on the canvas"""
        for curve in self.curves:
            curve_points = [
                self.points[curve[0]],
                self.points[curve[1]],
                self.points[curve[2]],
                self.points[curve[3]]
            ]
            curve = self.bezier_curve(curve_points)
            for i in range(len(curve)-1):
                self.canvas.create_line(curve[i][0], curve[i][1], curve[i+1][0], curve[i+1][1], fill='red', width=2)

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
        
    def scaling_inputs(self):
        """Handle scaling inputs"""
        # popout window
        self.current_transformation = "scaling"
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Scaling")
        popout_window.geometry("300x150")
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
        # handle the popout window button
        def handle_popout_button():
            x = 1 if x_popout_entry.get() == "" else x_popout_entry.get()
            y = 1 if y_popout_entry.get() == "" else y_popout_entry.get()
            if x == '-':
                x = -1
            if y == '-':
                y = -1
            self.submit([float(x), float(y)])
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
        popout_label = tk.Label(popout_window, text="Enter the rotation angle", bg="white")
        popout_label.pack()
        # create a label for x scaling
        popout_label = tk.Label(popout_window, text="Angle", bg="white")
        popout_label.pack()
        # create an entry for x scaling
        angle_popout_entry = tk.Entry(popout_window)
        # allow only float numbers
        angle_popout_entry.configure(validate="key", validatecommand=(self.root.register(self.validate_floats), "%P"))
        angle_popout_entry.pack()
        # handle the popout window buttons
        def handle_radians():
            angle = 0 if angle_popout_entry.get() == "" or angle_popout_entry.get() == "-"  else float(angle_popout_entry.get())
            self.submit([angle])
            popout_window.destroy()
        def degrees_to_radians():
            degree = 0 if angle_popout_entry.get() == "" or angle_popout_entry.get() == "-"  else float(angle_popout_entry.get())
            radian = degree * (math.pi/180)
            self.submit([radian])
            popout_window.destroy()
        # create buttons for the popout window
        popout_button = tk.Button(popout_window, text="Radians", command=handle_radians)
        popout_button.pack()
        popout_button = tk.Button(popout_window, text="Degrees", command=degrees_to_radians)
        popout_button.pack()
        
    def translate_inputs(self):
        """Handle translation inputs"""
        # change cursor to be draggable and get the draging points
        self.current_transformation = "translation"
        self.canvas.configure(cursor="fleur")
        self.canvas.bind("<Button-1>", self.handle_translate_click)
        self.root.bind("<Motion>", self.handle_translate_drag)
        self.canvas.bind("<ButtonRelease-1>", self.handle_translate_release)

    def handle_translate_click(self, event):
        """Get the start point of the translation"""
        self.translate_start_point = [event.x, event.y]
        self.translate_end_point = [event.x, event.y]

    def handle_translate_drag(self, event):
        # if the transformation is not translation, then disable the dragging
        if self.current_transformation != "translation":
            self.canvas.configure(cursor="arrow")
            self.canvas.unbind("<Button-1>")
            self.root.unbind("<Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.translate_start_point = [0, 0]
            self.translate_end_point = [0, 0]
            
    def handle_translate_release(self, event):
        """Get the end point of the translation and submit the transformation"""
        self.translate_end_point = [event.x, event.y]
        self.canvas.configure(cursor="arrow")
        self.canvas.unbind("<Button-1>")
        self.root.unbind("<Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if self.current_transformation == "translation":
            self.submit([self.translate_end_point[0]-self.translate_start_point[0], self.translate_end_point[1]-self.translate_start_point[1]])
        
    def mirroring_inputs(self):
        """Handle mirroring inputs"""
        # popout window
        self.current_transformation = "mirroring"
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Mirroring")
        popout_window.geometry("300x150")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white")
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Choose the mirroring axis", bg="white")
        popout_label.pack()
        # create a button for the popout window
        def handle_popout_button(axis):
            self.submit([axis])
            popout_window.destroy()
        x_popout_button = tk.Button(popout_window, text="X", command=lambda: handle_popout_button("x"))
        x_popout_button.pack()
        y_popout_button = tk.Button(popout_window, text="Y", command=lambda: handle_popout_button("y"))
        y_popout_button.pack()
        
    def shearing_inputs(self):
        """Handle shearing inputs"""
        # popout window
        self.current_transformation = "shearing"
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Shearing")
        popout_window.geometry("300x150")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white")
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Enter the shearing factor", bg="white")
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
        # create a button for the popout window
        def handle_popout_button():
            x = 0 if x_popout_entry.get() == "" or x_popout_entry.get() == "-"  else x_popout_entry.get()
            y = 0 if y_popout_entry.get() == "" or y_popout_entry.get() == "-"  else y_popout_entry.get()
            self.submit([float(x), float(y)])
            popout_window.destroy()
        popout_button = tk.Button(popout_window, text="Submit", command=handle_popout_button)
        popout_button.pack()
        
    def submit(self, params):
        """Submit the transformation"""
        if self.current_transformation == "scaling":
            self.scaling(params)
        elif self.current_transformation == "rotation":             
            self.rotation(params)
        elif self.current_transformation == "translation":             
            self.translation(params)
        elif self.current_transformation == "mirroring" :           
            self.mirroring(params)
        elif self.current_transformation == "shearing":             
            self.shearing(params)

        # draw the new shape
        self.draw_data()

    
    def rotation(self,params):
        """Rotate the shape"""
        angle=params[0]
        for i in range(len(self.points)):
            x = self.points[i][0]
            y = self.points[i][1]
            self.points[i][0] = self.mass_center[0] + (x-self.mass_center[0])*np.cos(angle) - (y-self.mass_center[1])*np.sin(angle)
            self.points[i][1] = self.mass_center[1] + (x-self.mass_center[0])*np.sin(angle) + (y-self.mass_center[1])*np.cos(angle)

    def translation(self,params):
        """Translate the shape"""
        for i in range(len(self.points)):
            self.points[i][0] += params[0]
            self.points[i][1] += params[1]
        self.mass_center = self.calculate_mass_center()
        
    def mirroring(self,params):
        """Mirror the shape"""
        axis=params[0]
        if(axis):
            if axis=="x":
                for i in range(len(self.points)):
                    self.points[i][0] = 2*self.mass_center[0] - self.points[i][0]
            elif axis=="y":
                for i in range(len(self.points)):
                    self.points[i][1] = 2*self.mass_center[1] - self.points[i][1]

    def scaling(self,params):
        """Scale the shape"""
        sx=params[0] #mult x
        sy=params[1]  #mult y

        if sx and sy: 
            for i in range(len(self.points)):
                self.points[i][0] = self.mass_center[0] + (self.points[i][0]-self.mass_center[0])*sx
                self.points[i][1] = self.mass_center[1] + (self.points[i][1]-self.mass_center[1])*sy
            # scale circle radius
            for circle in self.circles:
                circle[1] *= sx
        
    def shearing(self,params):
        """Shear the shape"""
        a=params[0]
        b=params[1]
        if a:
            for i in range(len(self.points)):
                self.points[i][0] += a*(self.points[i][1] - self.mass_center[1])
        if b:
            for i in range(len(self.points)):
                self.points[i][1] += b*(self.points[i][0] - self.mass_center[0]) 
        self.mass_center = self.calculate_mass_center()
    
    def center(self):
        """Center the shape"""
        self.mass_center = self.calculate_mass_center()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x_translation = width/2 - self.mass_center[0]
        y_translation = height/2 - self.mass_center[1]
        self.translation([x_translation, y_translation])
        self.draw_data()

    def clear(self):
        """Clear the canvas"""
        self.canvas.delete("all")
        self.points = []
        self.lines = []
        self.circles = []
        self.curves = []
        self.mass_center = [0, 0]
        self.disable_transformations()

    def readJson(self, filename):
        """read the json file and return the data """
        with open(filename, 'r') as f:
            # Load the data from the file
            data = json.load(f)
            return data

    def calculate_mass_center(self):
        """calculate the mass center of the shape"""
        x_sum = 0
        y_sum = 0
        for point in self.points:
            x_sum += point[0]
            y_sum += point[1]

        return [0 if len(self.points) == 0 else x_sum/len(self.points), 0 if len(self.points) == 0 else y_sum/len(self.points)]
    
    def extractShapesFromData(self, jsonData):
        """extract the shapes from the json data to separate variables"""
        self.clear()
        try:
            self.points = jsonData['points']
            self.lines = jsonData['lines']
            self.circles = jsonData['circles']
            self.curves = jsonData['curves']
            self.mass_center = self.calculate_mass_center()
        except Exception:
            messagebox.showerror("Error", "Json format is not valid.")
            return


    def openHelpWindow(self):
        """handle help choice from the menu bar and open the help window"""
        # popout window
        popout_window = tk.Toplevel(self.root)
        popout_window.title("Help")
        popout_window.geometry("600x200")
        popout_window.resizable(False, False)
        popout_window.configure(bg="white",padx=10,pady=10)
        # create a label for the popout window
        popout_label = tk.Label(popout_window, text="Hey, welcome !\n\nOptions:\n1- Upload New File- json format:\n{\t'points':[[x,y]...],\n\t'lines':[[pointIndex,pointIndex]...],\n\t'circles':[[pointIndex,R]...],\n\t'curves':[[pointIndex,pointIndex,pointIndex,pointIndex]...]\n}\n2- Choose transformation: Scale, Rotate, Translate, Mirror, Shear, Fit, Center \n3- Clear window- press clear \n4- Exit- press exit\n\n\n\n* Empty transformation values have no effect.",  justify=tk.LEFT, bg="white" )
        popout_label.pack(side='left')

    def fitWindow(self):
        """fit the shape to the window"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x_min = min(self.points, key=lambda point: point[0])[0]
        y_min = min(self.points, key=lambda point: point[1])[1]

        self.translation([-x_min, -y_min])

        x_max = max(self.points, key=lambda point: point[0])[0]
        y_max = max(self.points, key=lambda point: point[1])[1]

        x_scale = width/(x_max)
        y_scale = height/(y_max)
        scale = 0.7*min(x_scale, y_scale)
        self.scaling([scale, scale])
        
        self.center()

        self.draw_data()
    
    def disable_transformations(self):
        """disable the transformations button"""
        self.menubar.entryconfig('Transformations', state='disabled')


    def enable_transformations(self):
        """enable the transformations button"""
        self.menubar.entryconfig('Transformations', state='normal')
            
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
        transform_menu.add_command(label='Translate',command=self.translate_inputs)
        transform_menu.add_command(label='Mirror',command=self.mirroring_inputs)
        transform_menu.add_command(label='Shear',command=self.shearing_inputs)
        transform_menu.add_command(label='Fit',command=self.fitWindow)
        transform_menu.add_command(label='Center',command=self.center)

        self.menubar.entryconfig('Transformations', state='disabled')

        self.menubar.add_command(label="Clear", command=self.clear)
        self.menubar.add_command(label="Exit", command=root.destroy)
        self.menubar.add_command(label="Help", command=self.openHelpWindow)

        self.canvas = tk.Canvas(
            root,
            width=width,
            height=height,
            bg='black'
        )
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.root = root
        return root

    def draw_data(self):
        """draw the shape on the canvas"""
        self.canvas.delete("all")
        self.draw_lines()
        self.draw_circles()
        self.draw_bezier_curves()

    def update_data(self, file_path):
        """update the data from the json file"""
        if file_path == '':
            return
        data=self.readJson(file_path)
        self.extractShapesFromData(data)
        self.fitWindow()
        self.draw_data()
        self.enable_transformations()

    def upload_file(self):
        """upload a json file"""
        # Open a file dialog window
        file_path = filedialog.askopenfilename(initialdir="/",title="select a file",filetypes=(("json files","*.json"),("all files",  "*.*")))
        self.update_data(file_path)


if __name__ == "__main__":
    app=App()
    root=app.createMenu()
    root.mainloop()