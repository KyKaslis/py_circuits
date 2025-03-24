from components.component import Component

class cap(Component):
    def __init__(self, x1, y1, canvas):
        super().__init__(canvas)
        Component.number_of_capacitors += 1
        self.nol = 2
        self.x_coord.append(x1)
        self.y_coord.append(y1)
        self.x_coord.append(x1)
        self.y_coord.append(y1 + 80)
        self.capacitance= 0  # Farads

        x_shape = [0, 0, -25, 25]
        y_shape = [0, 35, 35, 35]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = [0, 0, -25, 25]
        y_shape = [80, 45, 45, 45]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        self.name = "C" + str(Component.number_of_capacitors) + " " + str(self.capacitance)