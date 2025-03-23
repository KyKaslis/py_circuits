from components.component import Component


class source(Component):
    def __init__(self, x1, y1, canvas):
        super().__init__(canvas)
        Component.number_of_sources += 1
        self.nol = 2
        self.x_coord.append(x1)
        self.y_coord.append(y1)
        self.x_coord.append(x1)
        self.y_coord.append(y1+80)
        self.canvas = canvas

        self.amplitude = 0 # Volts
        self.frequency = 0 # Hz
        self.mode = "DC" if self.frequency == 0 else str(self.frequency) + " Hz"
        self.name = "Src" + str(Component.number_of_sources) + " " + str(self.amplitude) + " " + self.mode

        x_shape = [0, 0, -25, 25]
        y_shape = [0, 35, 35, 35]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = [0, 0, 10, -10]
        y_shape = [80, 45, 45, 45]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])