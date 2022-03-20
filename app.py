import json

import numpy
from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template, jsonify, request
from gevent.pywsgi import WSGIServer
from resources.statue import Statue
from resources.pattern import Pattern
from typing import Optional, List
import os
import urllib.parse


class App:
    errorReturn = {"result": "error"}
    successReturn = {"result": "success"}

    def __init__(self):
        self.patternDir = "patterns"
        self.patterns = {}
        self.currentPattern = None
        self.currentTime = 0

        self.statue = Statue()
        self.statue.load_conversion_map("/resources/Structure Control - CrystalControl.csv")

        self.app = Flask(__name__)
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.server = None

        self.init_web_interface()

    def init_web_interface(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/api/list_patterns")
        def get_patterns():
            names = [{"safeName": i, "displayName": urllib.parse.unquote(i)} for i in self.get_pattern_names()]
            return jsonify({"patterns": names, **self.successReturn})

        @self.app.route("/api/create_pattern")
        def create_pattern():
            name = request.args.get("name", None)
            if name:
                if self.create_pattern(name):
                    return jsonify(self.successReturn)
            return jsonify(self.errorReturn)

        @self.app.route("/api/remove_pattern")
        def remove_pattern():
            name = request.args.get("name")
            if name:
                if self.remove_pattern(name):
                    return jsonify(self.successReturn)
            return jsonify(self.errorReturn)

        @self.app.route("/api/edit_pattern")
        def edit_pattern():
            return jsonify(self.successReturn)

        @self.app.route("/api/pattern_info")
        def pattern_info():
            name = request.args.get("name")
            pattern = self.get_pattern(name)
            if pattern:
                min_, max_ = pattern.get_min_and_max()
                return jsonify({"safeName": name,
                                "displayName": urllib.parse.unquote(name),
                                "animated": pattern.is_animated(),
                                "keyframes": [i.get_id() for i in pattern.get_keyframes()],
                                "minTime": min_,
                                "maxTime": max_,
                                **self.successReturn})
            return jsonify({**self.errorReturn, **self.errorReturn})

        @self.app.route("/api/create_keyframe")
        def create_keyframe():
            name = request.args.get("name")
            position = request.args.get("position", 0)
            try:
                position = float(position)
            except ValueError:
                pass
            except TypeError:
                pass
            pattern = self.get_pattern(name)
            if pattern:
                keyframe = pattern.add_keyframe(position)
                return jsonify({"id": keyframe.get_id(),
                                "position": keyframe.get_position(),
                                "state": keyframe.get_state().tolist(),
                                **self.successReturn})
            return jsonify(self.errorReturn)

        @self.app.route("/api/remove_keyframe")
        def remove_keyframe():
            name = request.args.get("name")
            id_ = request.args.get("id")
            pattern = self.get_pattern(name)
            try:
                id_ = int(id_)
            except ValueError:
                pass
            if pattern and pattern.has_keyframe(id_):
                pattern.remove_keyframe(id_)
                return jsonify(self.successReturn)
            return jsonify(self.errorReturn)

        @self.app.route("/api/edit_keyframe")
        def edit_keyframe():
            name = request.args.get("name")
            id_ = request.args.get("id")
            position = request.args.get("position")
            state = request.args.get("state")
            try:
                id_ = int(id_)
            except ValueError:
                pass
            except TypeError:
                pass
            try:
                position = float(position)
            except ValueError:
                pass
            except TypeError:
                pass
            try:
                state = urllib.parse.unquote(state)
                state = json.loads(state)
                state = numpy.array(state, dtype=">i1")
            except Exception:
                state = None
            pattern = self.get_pattern(name)
            if pattern and pattern.has_keyframe(id_):
                keyframe = pattern.get_keyframe(id_)
                if position:
                    keyframe.set_position(position)
                if state:
                    keyframe.set_state(state)
                return jsonify({"id": keyframe.get_id(),
                                "position": keyframe.get_position(),
                                "state": keyframe.get_state().tolist(),
                                **self.successReturn})

            return jsonify(self.errorReturn)

        @self.app.route("/api/keyframe_info")
        def keyframe_info():
            name = request.args.get("name")
            id_ = request.args.get("id")
            try:
                id_ = int(id_)
            except ValueError:
                pass
            except TypeError:
                pass
            pattern = self.get_pattern(name)
            if pattern:
                keyframe = pattern.get_keyframe(id_)
                if keyframe:
                    return jsonify({"id": id_,
                                    "position": keyframe.get_position(),
                                    "state": keyframe.get_state().tolist(),
                                    **self.successReturn})
            return jsonify(self.errorReturn)

        @self.app.route("/api/edit_statue")
        def edit_statue():
            currentPattern = request.args.get("current")
            currentTime = request.args.get("time")

            if currentPattern in self.patterns:
                self.set_current_pattern(currentPattern)

            if currentTime:
                self.set_current_time(currentTime)

            return jsonify({"currentPattern": self.currentPattern,
                            "currentTime": self.currentTime,
                            "currentState": self.statue.get_state().tolist(),
                            "isConnected": self.statue.is_connected(),
                            **self.successReturn})

        @self.app.route("/api/statue_info")
        def statue_info():
            return jsonify({"currentPattern": self.currentPattern,
                            "currentTime": self.currentTime,
                            "currentState": self.statue.get_state().tolist(),
                            "isConnected": self.statue.is_connected(),
                            **self.successReturn})

        self.server = WSGIServer(("127.0.0.1", 5000), self.app)

    def run_forever(self):
        self.server.serve_forever()

    def load_all_patterns(self):
        for file in (os.path.join(self.patternDir, i) for i in os.listdir(self.patternDir)):
            pattern = Pattern.read_from_file(file)
            if pattern.get_name() not in self.patterns:
                self.patterns[pattern.get_name()] = pattern

    def save_all_patterns(self):
        for pattern_name in self.patterns:
            pattern = self.patterns[pattern_name]
            pattern.save_to_file(os.path.join(self.patternDir, pattern_name))

    def create_pattern(self, name: str):
        name = urllib.parse.quote(name)
        if name not in self.patterns:
            pattern = Pattern(self.statue.get_shape(), name)
            self.patterns[name] = pattern
            return True
        return False

    def remove_pattern(self, name: str):
        if name in self.patterns:
            if self.currentPattern == name:
                self.currentPattern = None
            del self.patterns[name]

            os.remove(os.path.join(self.patternDir, name))
            return True
        return False

    def get_pattern_names(self) -> List[str]:
        return list(self.patterns.keys())

    def get_pattern(self, name: str) -> Optional[Pattern]:
        return self.patterns.get(name)

    def set_current_time(self, t):
        self.currentTime = t

    def set_current_pattern(self, pattern):
        if pattern in self.patterns:
            self.currentPattern = pattern


if __name__ == "__main__":
    a = App()
    a.load_all_patterns()
    a.create_pattern("test2")
    p = a.get_pattern("test2")
    p.add_keyframe(0)
    a.run_forever()
