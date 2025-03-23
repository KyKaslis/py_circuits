from fontTools.merge.util import first


class Component:

    number_of_resistors = 0
    number_of_wires = 0
    number_of_grounds = 0
    number_of_sources = 0

    def __init__(self, canvas):
        self.C = canvas
        self.x_coord = [] # x-coordinate to be placed, first node 1 then node 2
        self.y_coord = [] # y-coordinate to be placed, first node 1 then node 2
        self.shape = [] # the shape of the components
        self.canvas_id = [] # the unique id in the canvas
        self.name = ""
        self.nol = 0 # number of lines used to draw the component
        self.hl = 0 # if 1 it has been highlighted by the user, otherwise 0
        self.label_hl = 0 # if 1 the label of this component has been highlighted, otherwise 0
        self.label_id = -1 # the unique id of the label
        self.polarity = [] # the polarity of the current (to be used by the engine)
        self.neighbors = [[],[]] # the components electrically connected to this component (left list node 1, right list node 2)

    def selfdelete(self):
        for i in range(self.nol):
            self.C.delete(self.canvas_id[i])
            if self.name[0] != "W":
                self.C.delete(self.label_id)
        print("Deleting " + self.name)

    def drawit(self):
        for i in range(self.nol):
            cid = self.C.create_line(self.shape[i], activefill='red', width=3)
            self.canvas_id.append(cid)

    def highlighted(self):
        for i in range(self.nol):
            self.C.itemconfig(self.canvas_id[i], fill='red')

    def label_highlighted(self):
        self.C.itemconfig(self.label_id, fill='red')

    def unhighlighted(self):
        for i in range(self.nol):
            self.C.itemconfig(self.canvas_id[i], fill='black')

    def label_unhighlighted(self):
        self.C.itemconfig(self.label_id, fill='blue')

    def rotate(self):
        print("Rotating " + self.name)
        a = self.C.coords(self.canvas_id[0])
        initial_vector_x = a[0]
        initial_vector_y = a[1]
        for i in range(self.nol):
            x_coordinates = []
            y_coordinates = []
            coordinates = self.C.coords(self.canvas_id[i])
            for k in range(len(coordinates)):
                if k % 2 == 0:
                    x_coordinates.append(coordinates[k])
                else:
                    y_coordinates.append(coordinates[k])

            x_coordinates_1 = [dummy-initial_vector_x for dummy in x_coordinates]
            y_coordinates_1 = [dummy-initial_vector_y for dummy in y_coordinates]

            x_coordinates_2 = [-dummy for dummy in y_coordinates_1]
            y_coordinates_2 = [dummy for dummy in x_coordinates_1]

            x_coordinates_3 = [dummy+initial_vector_x for dummy in x_coordinates_2]
            y_coordinates_3 = [dummy+initial_vector_y for dummy in y_coordinates_2]

            self.C.coords(self.canvas_id[i], [val for pair in zip(x_coordinates_3, y_coordinates_3) for val in pair])

    def move_comp(self, dx, dy):
        for i in range(self.nol):
            x_coordinates = []
            y_coordinates = []
            coordinates = self.C.coords(self.canvas_id[i])
            for k in range(len(coordinates)):
                if k % 2 == 0:
                    x_coordinates.append(coordinates[k])
                else:
                    y_coordinates.append(coordinates[k])

            x_coordinates = [x+dx for x in x_coordinates]
            y_coordinates = [y+dy for y in y_coordinates]

            self.C.coords(self.canvas_id[i], [val for pair in zip(x_coordinates, y_coordinates) for val in pair])

        if self.name[0] != "W":
            x_coordinates = []
            y_coordinates = []
            coordinates = self.C.coords(self.label_id)
            for k in range(len(coordinates)):
                if k % 2 == 0:
                    x_coordinates.append(coordinates[k])
                else:
                    y_coordinates.append(coordinates[k])

            x_coordinates = [x + dx for x in x_coordinates]
            y_coordinates = [y + dy for y in y_coordinates]

            self.C.coords(self.label_id, [val for pair in zip(x_coordinates, y_coordinates) for val in pair])

    def move_label(self, dx, dy):
        x_coordinates = []
        y_coordinates = []
        coordinates = self.C.coords(self.label_id)
        for k in range(len(coordinates)):
            if k % 2 == 0:
                x_coordinates.append(coordinates[k])
            else:
                y_coordinates.append(coordinates[k])

        x_coordinates = [x + dx for x in x_coordinates]
        y_coordinates = [y + dy for y in y_coordinates]

        self.C.coords(self.label_id, [val for pair in zip(x_coordinates, y_coordinates) for val in pair])

    def showname(self):
        if self.name[0] == "R":
            if self.label_id == -1:
                self.label_id = self.C.create_text((self.x_coord[0]+self.x_coord[1])/2, self.y_coord[0]-30, fill = "blue", font = "Times 15", text = self.name)
            else:
                self.C.delete(self.label_id) # label needs to be deleted to get updated
                self.label_id = self.C.create_text((self.x_coord[0]+self.x_coord[1])/2, self.y_coord[0]-30, fill = "blue", font = "Times 15", text = self.name)
        elif self.name[0] == "S":
            if self.label_id == -1:
                self.label_id = self.C.create_text(self.x_coord[0]-80, -15+self.y_coord[1], fill = "blue", font = "Times 15", text = self.name)
            else:
                self.C.delete(self.label_id)  # label needs to be deleted to get updated
                self.label_id = self.C.create_text(self.x_coord[0]-80, -15+self.y_coord[1], fill = "blue", font = "Times 15", text = self.name)
        elif self.name[0] == "G":
            self.label_id = self.C.create_text(self.x_coord[0]-30, self.y_coord[0]+70, fill = "blue", font = "Times 15", text = self.name)