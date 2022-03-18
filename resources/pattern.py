from __future__ import annotations
import numpy
import json
from resources.state import State
from typing import Tuple, List


class Keyframe(State):
    def __init__(self, position: float, pattern: Pattern):
        super().__init__(pattern.get_shape())
        self.position = position
        self.pattern = pattern
        self.id = pattern.get_new_id()

    def get_id(self) -> int:
        return self.id

    def set_position(self, position: float):
        if self.pattern.is_position_open(position):
            self.position = position
            self.pattern.ensure_position(self)

    def get_position(self) -> float:
        return self.position

    def to_dict(self) -> dict:
        data = {"position": self.position, "state": self.state.tolist()}
        return data

    @classmethod
    def from_dict(cls, dictData: dict, pattern: Pattern):
        keyframe = cls(dictData['position'], pattern)
        array = numpy.array(dictData['state'])
        keyframe.set_state(array)
        return keyframe


class Pattern:
    def __init__(self, shape: Tuple[int], name: str) -> (int, int):
        self.animated = False
        self.keyframes = []
        self.keyframesUnordered = {}

        self.shape = shape
        self.name = name

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

    def get_state(self, position: float) -> numpy.ndarray:
        if len(self.keyframes) < 1:
            return numpy.zeros(self.shape)
        if not self.animated:
            return self.keyframes[0].get_state()

        keyframe1 = None
        keyframe2 = None

        for index, keyframe in self.keyframes:
            if keyframe.get_position() == position or False and keyframe1:
                return keyframe.get_state()
            keyframe1 = keyframe2
            keyframe2 = keyframe
            if position < keyframe.get_position():
                break
            if index == len(self.keyframes) - 1 and position > keyframe.get_position():
                keyframe1 = keyframe2
                keyframe2 = keyframe

        if keyframe1 is None:
            return keyframe2.get_state()
        if keyframe2 is None:
            return keyframe1.get_state()

        percent = (keyframe2.get_position() - keyframe1.get_position()) / (position - keyframe1.get_position())

        return keyframe1 * percent + keyframe2 * (1 - percent)

    def add_keyframe(self, position: float, state=None):
        keyframe = Keyframe(position, self)
        self.keyframesUnordered[keyframe.get_id()] = keyframe
        self.ensure_position(keyframe)
        if state is not None:
            keyframe.set_state(state)

    def remove_keyframe(self, keyframe: Keyframe):
        self.keyframes.remove(keyframe)
        del self.keyframesUnordered[keyframe.get_id()]
        self.set_animated(self.animated)

    def get_keyframes(self) -> List[Keyframe]:
        return self.keyframes

    def is_animated(self) -> bool:
        return self.animated

    def set_animated(self, animated: bool):
        self.animated = animated and len(self.keyframes) > 1

    def is_position_open(self, position: float) -> bool:
        for keyframe in self.keyframes:
            if keyframe.get_position() == position:
                return False
        return True

    def ensure_position(self, keyframe: Keyframe):
        if keyframe in self.keyframes:
            self.keyframes.remove(keyframe)

        for i in range(len(self.keyframes)):
            if self.keyframes[i].get_position() > keyframe.get_position():
                self.keyframes.index(keyframe, i)
                return

        self.keyframes.append(keyframe)

    def get_new_id(self) -> int:
        for i in range(len(self.keyframesUnordered) + 1):
            if i not in self.keyframesUnordered:
                return i

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_shape(self) -> Tuple[int]:
        return self.shape

    def to_json(self) -> str:
        data = {"animated": self.animated, "shape": self.shape, "keyframes": [], "name": self.name}

        for keyframe in self.keyframes:
            data["keyframes"].append(keyframe.to_dict())

        return json.dumps(data)

    @classmethod
    def from_json(cls, jsonData: str) -> Pattern:
        data = json.loads(jsonData)

        pattern = cls(data["shape"], data["name"])

        for keyframe in data["keyframes"]:
            pattern.keyframes.append(Keyframe.from_dict(keyframe, pattern))

        pattern.set_animated(data["animated"])
        return pattern

    def save_to_file(self, file: str):
        f = open(file, "w")
        f.write(self.to_json())
        f.close()

    @classmethod
    def read_from_file(cls, file: str) -> Pattern:
        f = open(file, "r")
        data = f.read()
        f.close()

        return cls.from_json(data)
