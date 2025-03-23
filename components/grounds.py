from components.component import Component


class ground(Component):
    def __init__(self, x1, y1, canvas):
        super().__init__(canvas)
        Component.number_of_grounds += 1
        self.nol = 3
        self.name = "GND" + str(Component.number_of_grounds)
        self.x_coord.append(x1)
        self.y_coord.append(y1)

        x_shape = [0, 0, -25, 25]
        y_shape = [0, 35, 35, 35]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = [-15, 15]
        y_shape = [45, 45]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = [-5, 5]
        y_shape = [55, 55]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])