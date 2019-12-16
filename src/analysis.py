import json
from werkzeug.utils import redirect
from flask import Flask, jsonify, render_template, request, url_for
# from src.__init__ import main
app = Flask(__name__)

@app.route("/one")
def one():
    return render_template("one.html")

@app.route("/a")
def a():
    return render_template("2.html")

@app.route("/3")
def b():
    return render_template("3.html")

@app.route("/map")
def c():
    return render_template("map.html")

@app.route("/map1")
def d():
    return render_template("map1.html")

@app.route("/map2")
def e():
    return render_template("map2.html")

@app.route("/4")
def f():
    return render_template("4.html")

@app.route("/index")
def index():
    return render_template("Base.html")


if __name__ == '__main__':
    # main()
    app.run(host='127.0.0.1', port=8080, debug=True)