from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from resources.statue import Statue


statue = Statue()
statue.load_conversion_map("/resources/Structure Control - CrystalControl.csv")

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    server = WSGIServer(("127.0.0.1", 5000), app)
    server.serve_forever()
