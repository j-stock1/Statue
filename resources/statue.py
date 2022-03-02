import serial
import time
import numpy


class Color:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

    def ensure_values(self):
        if self.r < 0:
            self.r = 0
        elif self.r > 255:
            self.r = 255

        if self.g < 0:
            self.g = 0
        elif self.g > 255:
            self.g = 255

        if self.b < 0:
            self.b = 0
        elif self.b > 255:
            self.b = 255

    def get_r(self):
        return self.r

    def get_g(self):
        return self.g

    def get_b(self):
        return self.b

    def get_tuple(self):
        return self.r, self.g, self.b

    def set_r(self, r):
        self.r = r
        self.ensure_values()

    def set_g(self, g):
        self.g = g
        self.ensure_values()

    def set_b(self, b):
        self.b = b
        self.ensure_values()

    def set_tuple(self, tuple_):
        self.r = tuple_[0]
        self.g = tuple_[0]
        self.b = tuple_[0]
        self.ensure_values()


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


class Statue:
    muxSize = 16
    buffer_len = muxSize * muxSize * 2 * 3

    rings = 17
    crystals = 22

    def __init__(self):
        self.serial = None
        #self.serial = serial.Serial(port='COM6', baudrate=115200, timeout=0.1)
        self.state = numpy.zeros((self.rings, self.crystals, 3))
        self.exportedState = numpy.zeros((self.muxSize * 2, self.muxSize, 3), dtype=">i1")
        self.exportedState[0][0][0] = 1
        self.exportedState[0][0][1] = 2
        self.exportedState[0][0][2] = 3
        print(self.state.shape)

    @allow_rgb
    def set_column(self, column, color):
        for ring in range(self.rings):
            self.state[ring][column] = color.get_tuple()

    @allow_rgb
    def set_crystal(self, ring, crystal, color):
        self.state[ring][crystal] = color.get_tuple()

    @allow_rgb
    def set_ring(self, ring, color):
        for crystal in range(self.crystals):
            self.state[ring][crystal] = color.get_tuple()

    @allow_rgb
    def set_statue(self, color):
        for ring in range(self.rings):
            for crystal in range(self.crystals):
                self.state[ring][crystal] = color.get_tuple()

    def update_statue(self):
        output = numpy.ndarray.tobytes(self.exportedState)
        if self.serial:
            self.serial.write(output)

            while True:
                recv = self.serial.read(1)
                if len(recv) == 1:
                    break
