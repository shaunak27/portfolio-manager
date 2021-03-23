from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/index.html")
def dashboard():
    return render_template("index.html")

@app.route("/register.html")
def registration():
    return render_template("register.html")

@app.route("/chart.html")
def charts():
    return render_template("chart.html")

@app.route("/card.html")
def news():
    return render_template("card.html")

@app.route("/table.html")
def WatchList():
    return render_template("table.html")


if __name__ == "__main__":
    app.run(debug=True)
