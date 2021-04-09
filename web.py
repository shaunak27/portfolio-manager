from flask import Flask, redirect, url_for, render_template
from forms import LoginForm, RegForm, holdingForm, watchlistForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myproj'

@app.route("/login.html",methods = ["GET","POST"])
def login():
    form = LoginForm()
    return render_template("login.html",form=form)

@app.route("/index.html",methods=["GET","POST"])
def dashboard():
    form = holdingForm()
    return render_template("index.html",form=form)

@app.route("/",methods=["GET","POST"])
def home():
    form = holdingForm()
    return render_template("index.html",form=form)

@app.route("/register.html", methods=["GET","POST"])
def registration():
    form = RegForm()
    return render_template("register.html",form=form)

@app.route("/chart.html")
def charts():
    return render_template("chart.html")

@app.route("/card.html")
def news():
    return render_template("card.html")

@app.route("/table.html", methods=["GET","POST"])
def WatchList():
    form = watchlistForm()
    return render_template("table.html",form=form)


if __name__ == "__main__":
    app.run(debug=True)
