from components.component import Component

class wire(Component):
    def __init__(self, x1, y1, x2, y2, canvas):
        super().__init__(canvas)
        Component.number_of_wires += 1
        self.nol = 1
        self.name = "Wire " + str(Component.number_of_wires)
        self.x_coord = []
        self.x_coord.append(x1)
        self.x_coord.append(x2)
        self.y_coord = []
        self.y_coord.append(y1)
        self.y_coord.append(y2)
        self.shape.append([x1, y1, x2, y2])