import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        return redirect(url_for("greet", name=name))
    return render_template("index.html")


@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", name=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
