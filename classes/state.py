import numpy
from typing import Tuple

from classes.color import Color


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
    def __init__(self, shape: Tuple[int, ...]):
        self.shape = shape
        self.state = numpy.zeros(shape, dtype=">i1")

    def get_shape(self) -> Tuple[int]:
        return self.state.shape

    def set_state(self, state: numpy.ndarray):
        if state.shape == self.state.shape:
            self.state = state.copy()

    def get_state(self) -> numpy.ndarray:
        return self.state

    @allow_rgb
    def set_column(self, column: int, color: Color):
        for ring in range(self.shape[0]):
            self.state[ring][column] = color.get_tuple()

    @allow_rgb
    def set_crystal(self, ring: int, crystal: int, color: Color):
        self.state[ring][crystal] = color.get_tuple()

    @allow_rgb
    def set_ring(self, ring: int, color: Color):
        for crystal in range(self.shape[1]):
            self.state[ring][crystal] = color.get_tuple()

    @allow_rgb
    def set_statue(self, color: Color):
        for ring in range(self.shape[0]):
            for crystal in range(self.shape[1]):
                self.state[ring][crystal] = color.get_tuple()
