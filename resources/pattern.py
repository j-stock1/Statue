import numpy


class Keyframe:
    def __init__(self, position, pattern):
        self.position = position
        self.pattern = pattern
        self.id = pattern.get_new_id()

        self.state = numpy.zeros(self.pattern.get_shape())

    def get_id(self):
        return self.id

    def set_state(self, state):
        if state.shape == self.pattern.get_shape():
            self.state = state

    def get_state(self):
        return self.state

    def set_position(self, position):
        if self.pattern.is_position_open(position):
            self.position = position
            self.pattern.ensure_position(self)

    def get_position(self):
        return self.state


class Pattern:
    def __init__(self, shape):
        self.animated = False
        self.keyframes = []
        self.keyframesUnordered = {}

        self.shape = shape

    def get_min_and_max(self):
        if len(self.keyframes) < 1:
            return 0, 0
        if not self.animated:
            return 0, 0
        min_ = self.keyframes[0].get_position()
        max_ = self.keyframes[0].get_position()

        for keyframe in self.keyframes[1:]:
            if keyframe.get_position() < min_:
                min_ = keyframe.get_position()
            if keyframe.get_position() > max_:
                max_ = keyframe.get_position()
        return min_, max_

    def get_state(self, position):
        if len(self.keyframes) < 1:
            return numpy.zeros(self.shape)
        if not self.animated:
            return self.keyframes[0].get_state()







    def add_keyframe(self, position, state=None):
        keyframe = Keyframe(position, self)
        self.keyframesUnordered[keyframe.get_id()] = keyframe
        self.ensure_position(keyframe)
        if state is not None:
            keyframe.set_state(state)

    def remove_keyframe(self, keyframe):
        self.keyframes.remove(keyframe)
        del self.keyframesUnordered[keyframe.get_id()]
        self.set_animated(self.animated)

    def get_keyframes(self):
        return self.keyframes

    def is_animated(self):
        return self.animated

    def set_animated(self, animated):
        self.animated = animated and len(self.keyframes) > 1

    def is_position_open(self, position):
        for keyframe in self.keyframes:
            if keyframe.get_position() == position:
                return False
        return True

    def ensure_position(self, keyframe):
        if keyframe in self.keyframes:
            self.keyframes.remove(keyframe)

        for i in range(len(self.keyframes)):
            if self.keyframes[i].get_position() > keyframe.get_position():
                self.keyframes.index(keyframe, i)
                return

        self.keyframes.append(keyframe)

    def get_new_id(self):
        for i in range(len(self.keyframesUnordered) + 1):
            if i not in self.keyframesUnordered:
                return i

    def get_shape(self):
        return self.shape