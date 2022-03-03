import serial
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

    def __init__(self, dummyConnection=False, ):
        self.port = "COM6"
        self.baudrate = 115200
        self.dummyConnection = dummyConnection

        self.serial = None
        self.create_connection()

        self.state = numpy.zeros((self.rings, self.crystals, 3))
        self.convertMap = numpy.zeros((self.rings, self.crystals), dtype="int")
        self.exportedState = numpy.zeros((self.muxSize * 2, self.muxSize, 3), dtype=">i1")

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

    def is_connected(self):
        if self.serial is None:
            return False
        return self.serial.isOpen()

    def create_connection(self):
        if not self.is_connected() and not self.dummyConnection:
            try:
                self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=0.1)
            except serial.serialutil.SerialException:
                pass

    def close_connection(self):
        if self.is_connected():
            self.serial.close()
            self.serial = None

    def transform_colors(self):
        for ring in range(self.rings):
            for crystal in range(self.crystals):
                index = self.convertMap[ring][crystal]
                muxX = index % self.muxSize
                muxY = index // self.muxSize
                self.exportedState[muxY][muxX] = self.state[ring][crystal]

    def load_conversion_map(self, filePath):
        offset = 1, 3
        size = 44, 17

        try:
            with open(filePath) as f:
                data = f.read()
        except IOError:
            return False

        lines = data.split("\n")

        data_array = []

        for line_index, line in enumerate(lines):
            if offset[1] <= line_index <= offset[1] + size[1]:
                data_points = line.split(",")

                array_row = []
                dp = []

                for data_point_index, data_point in enumerate(data_points):
                    if offset[0] <= data_point_index <= offset[0] + size[0]:
                        if len(dp) > 0 and dp[0] == -1:
                            dp.append(-1)
                            array_row.append(dp)
                            dp = []
                            continue
                        try:
                            dp.append(int(data_point))
                        except ValueError:
                            dp.append(-1)

                        if len(dp) == 2:
                            array_row.append(dp)
                            dp = []
                data_array.append(array_row)
        data_array.reverse()
        for y in range(len(data_array)):
            for x in range(len(data_array[y])):
                x_value = data_array[y][x][1]
                y_value = data_array[y][x][0]
                if x_value == -1:
                    c = -1
                else:
                    c = y_value * self.crystals + x_value
                self.convertMap[y][x] = c

        return True

    def update_statue(self):
        self.transform_colors()
        output = numpy.ndarray.tobytes(self.exportedState)

        if self.serial:
            self.serial.write(output)

            while True:
                recv = self.serial.read(1)
                if len(recv) == 1:
                    break

    def upload_code(self, cppFile):
        self.close_connection()
        # UPLOAD CODE
        self.create_connection()
