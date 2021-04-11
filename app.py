from flask import Flask, redirect, url_for, render_template, request, flash, session
from forms import LoginForm, RegForm, holdingForm, watchlistForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask import Flask, redirect, url_for, render_template
from forms import LoginForm, RegForm, holdingForm, watchlistForm
from flask_migrate import Migrate
from stockprice import companydetails

app = Flask(__name__)
app.config["SECRET_KEY"] = "myproj"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///manager.sqlite3"
db = SQLAlchemy(app)
from models import *
migrate = Migrate(app, db)

@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Investor.query.filter_by(
            panid=request.form["panid"], password=request.form["password"]
        ).first()
        if user:
            session["logged_in"] = True
            session["username"] = user.username
            session["panid"] = user.panid
            return redirect(url_for("dashboard"))
        else:
            flash("Login details are Incorrect !")
            return redirect(url_for("login"))
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/index.html", methods=["GET", "POST"])
def dashboard():
    if session.get("logged_in") is None or session.get("panid") is None or session["logged_in"] == False:
        return redirect(url_for("login"))
    if request.method == "POST":
        data = Holdings(
            orderid=request.form["orderid"],
            stockname=request.form["stockname"],
            quantity=request.form["quantity"],
            date=datetime.strptime(request.form["date"], "%d/%m/%Y").date(),
            buyingprice=request.form["buyingprice"],
            panid=session['panid']
        )
        db.session.add(data)
        db.session.commit()
        flash("Record was successfully added")
        return redirect(url_for("dashboard"))
    records = Holdings.query.filter_by(
            panid = session['panid']
        ).all()
    form = holdingForm()
    return render_template("index.html", form=form,data=records)


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/register.html", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        user = Investor(
            panid=request.form["panid"],
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"],
        )
        db.session.add(user)
        db.session.commit()
        session["logged_in"] = True
        session["username"] = user.username
        session["register"] = user.panid
        flash("Record was successfully added")
        return redirect(url_for("dashboard"))
    form = RegForm()
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    session.pop("username", None)
    session.pop("panid", None)
    session["logged_in"] = False
    return redirect(url_for("login"))


@app.route("/chart.html")
def charts():
    return render_template("chart.html")


@app.route("/card.html")
def news():
    return render_template("card.html")


@app.route("/table.html", methods=["GET", "POST"])
def watchlist():
    if session.get("logged_in") is None or session.get("panid") is None or session["logged_in"] == False:
        return redirect(url_for("login"))
    if request.method == "POST":
        d = companydetails(request.form["stockname"].upper())
        if len(d) is 0 :
            flash("Entered Details could not be fetched !")
            return redirect(url_for("watchlist"))
        data = Watchlist(
            stockname=request.form["stockname"].upper(),
            cmp = d.get('cmp',0.0),
            marketcap= d.get('marketcap',0.0),
            sector = d.get('sector','none'),
            peratio = d.get('pe',0.0),
            panid=session['panid']
        )
        db.session.add(data)
        db.session.commit()
        flash("Record was successfully added")
        return redirect(url_for("watchlist"))
    records = Watchlist.query.filter_by(
            panid = session['panid']
        ).all()
    form = watchlistForm()
    return render_template("table.html", form=form,data=records)


if __name__ == "__main__":

    app.run(debug=True)
