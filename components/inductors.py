from components.component import Component
import numpy as np

class ind(Component):
    def __init__(self, x1, y1, canvas):
        super().__init__(canvas)
        Component.number_of_inductors += 1
        self.nol = 5
        self.x_coord.append(x1)
        self.y_coord.append(y1)
        self.x_coord.append(x1+135)
        self.y_coord.append(y1)
        self.inductance= 0  # Henry

        x_shape = [0, 40]
        y_shape = [0, 0]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = []
        y_shape = []
        for phi in range(361):
            x = 60+20*np.cos(np.deg2rad(180-phi))*(1-phi*(10/(360*20)))
            x_shape.append(x)
            y = -15*np.sin(np.deg2rad(180-phi))
            y_shape.append(y)

        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = []
        y_shape = []
        for phi in range(361):
            x = 70 + 20 * np.cos(np.deg2rad(180 - phi)) * (1 - phi * (10 / (360 * 20)))
            x_shape.append(x)
            y = -15 * np.sin(np.deg2rad(180 - phi))
            y_shape.append(y)

        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = []
        y_shape = []
        for phi in range(181):
            x = 80 + 20 * np.cos(np.deg2rad(180 - phi)) * (1 - phi * (10 / (360 * 20)))
            x_shape.append(x)
            y = -15 * np.sin(np.deg2rad(180 - phi))
            y_shape.append(y)

        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        x_shape = [95, 135]
        y_shape = [0, 0]
        self.x_shape = [*map(lambda a: a + x1, x_shape)]
        self.y_shape = [*map(lambda a: a + y1, y_shape)]
        self.shape.append([val for pair in zip(self.x_shape, self.y_shape) for val in pair])

        self.name = "L" + str(Component.number_of_capacitors) + " " + str(self.inductance)