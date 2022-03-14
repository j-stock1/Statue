import numpy
from resources.color import Color


def allow_rgb(funct):
    def fun(*args, **kwargs):
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], tuple) and len(args[i]) == 3:
                c = Color()
                c.set_tuple(args[i])
                args[i] = c

        funct(*args, **kwargs)
    return fun


class State:
    def __init__(self, shape):
        self.shape = shape
        self.state = numpy.zeros(shape)

    def get_shape(self):
        return self.state.shape

    def set_state(self, state):
        if state.shape == self.state.shape:
            self.state = state.copy()

    def get_state(self):
        return self.state

    @allow_rgb
    def set_column(self, column, color):
        for ring in range(self.shape[0]):
            self.state[ring][column] = color.get_tuple()

    @allow_rgb
    def set_crystal(self, ring, crystal, color):
        self.state[ring][crystal] = color.get_tuple()

    @allow_rgb
    def set_ring(self, ring, color):
        for crystal in range(self.shape[1]):
            self.state[ring][crystal] = color.get_tuple()

    @allow_rgb
    def set_statue(self, color):
        for ring in range(self.shape[0]):
            for crystal in range(self.shape[1]):
                self.state[ring][crystal] = color.get_tuple()
