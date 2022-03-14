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