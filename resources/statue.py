import serial
import numpy
from resources.state import State


class Statue(State):
    muxSize = 16
    buffer_len = muxSize * muxSize * 2 * 3

    rings = 17
    crystals = 22

    def __init__(self, dummyConnection=False, port="COM6", baudrate=115200):
        super().__init__((self.rings, self.crystals, 3))
        self.port = port
        self.baudrate = baudrate
        self.dummyConnection = dummyConnection

        self.serial = None
        self.create_connection()

        self.convertMap = numpy.zeros((self.rings, self.crystals), dtype="int")
        self.exportedState = numpy.zeros((self.muxSize * 2, self.muxSize, 3), dtype=">i1")

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
