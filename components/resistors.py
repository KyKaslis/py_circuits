from components.component import Component

class res(Component):
    def __init__(self, x1, y1, canvas):
        super().__init__(canvas)
        x_shape = [0, 10, 20, 40, 60, 80, 90, 100]
        y_shape = [0, 0, 10, -10, 10, -10, 0, 0]
        Component.number_of_resistors += 1
        self.nol = 1
        self.x_coord.append(x1)
        self.x_coord.append(x1+x_shape[-1])
        self.y_coord.append(y1)
        self.y_coord.append(y1)
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])
        self.resistance = 0 # Ohms
        self.name = "R" + str(Component.number_of_resistors) + " " + str(self.resistance)

