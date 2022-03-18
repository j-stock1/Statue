from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from resources.statue import Statue
from resources.pattern import Pattern
from typing import Optional
import os


class App:
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
        if name not in self.patterns:
            pattern = Pattern(self.statue.get_shape(), name)
            self.patterns[name] = pattern

    def remove_pattern(self, name: str):
        if name in self.patterns:
            if self.currentPattern == name:
                self.currentPattern = None
            del self.patterns[name]

            os.remove(os.path.join(self.patternDir, name))

    def get_pattern_names(self) -> list[str, ...]:
        return list(self.patterns.keys())

    def get_pattern(self, name: str) -> Optional[Pattern]:
        return self.patterns.get(name)


if __name__ == "__main__":
    a = App()
    a.load_all_patterns()
    a.run_forever()
