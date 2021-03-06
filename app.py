from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from forms import (
    LoginForm,
    RegForm,
    holdingForm,
    watchlistForm,
    LoginAdminForm,
    deleteUserForm,
    UserEditForm,
    MLForm,
    deleteholdingForm,
)
from flask_migrate import Migrate
from stockprice import companydetails
from getchartdata import get_chartdata
from stocknews import companynews
from sentiment import get_sentiment
from getmldata import getdata

app = Flask(__name__)
app.config["SECRET_KEY"] = "myproj"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///manager.sqlite3"
db = SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'tradecasttester@gmail.com'
app.config['MAIL_PASSWORD'] = 'TradeCast1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail= Mail(app)
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
            session['sentmail'] = 0
            return redirect(url_for("dashboard"))
        else:
            flash("Login details are Incorrect !")
            return redirect(url_for("login"))
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/loginAdmin.html", methods=["GET", "POST"])
def login_Admin():

    if request.method == "POST":
        admin = Admin.query.filter_by(
            loginid=request.form["loginid"],
            email=request.form["email"],
            password=request.form["password"],
        ).first()

        if admin:
            session["logged_in"] = True
            session["loginid"] = admin.loginid

            return redirect(url_for("dashboard_Admin"))
        else:
            flash("Login details are Incorrect !")
            return redirect(url_for("login_Admin"))
    form = LoginAdminForm()
    return render_template("loginAdmin.html", form=form)


@app.route("/enterml.html", methods=["GET", "POST"])
def enterml():

    if request.method == "POST":
        data = Watchlist.query.filter_by(stockname=request.form["stockname"]).first()

        if data:
            mldata = getdata(data.stockname, 5)
            return render_template("chart.html", data=mldata)
        else:
            flash("Entered company in not a part of your holdings !")
            return redirect(url_for("dashboard"))
    form = MLForm()
    return render_template("enterml.html", form=form)


@app.route("/indexAdmin.html", methods=["GET", "POST"])
def dashboard_Admin():
    users = Investor.query.all()
    if request.method == "POST":
        if request.form["btn"] == "submit":
            deleteuser = Investor.query.filter_by(panid=request.form["panid"]).first()
            if deleteuser is None:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("dashboard_Admin"))
            db.session.delete(deleteuser)
            db.session.commit()
            flash("Record was successfully deleted")
            return redirect(url_for("dashboard_Admin"))
        elif request.form["btn"] == "edit":

            edituser = Investor.query.filter_by(panid=request.form["panid"]).first()
            if edituser is None:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("dashboard_Admin"))
            edituser.username = request.form["username"]
            edituser.password = request.form["password"]
            edituser.email = request.form["email"]

            db.session.add(edituser)
            db.session.commit()
            flash("Record was successfully updated")
            return redirect(url_for("dashboard_Admin"))

    form = deleteUserForm()
    form1 = UserEditForm()
    return render_template("indexAdmin.html", users=users, form=form, form1=form1)


@app.route("/index.html", methods=["GET", "POST"])
def dashboard():
    if (
        session.get("logged_in") is None
        or session.get("panid") is None
        or session["logged_in"] == False
    ):
        return redirect(url_for("login"))
    if request.method == "POST":
        if request.form["btn"] == "submit":
            d = companydetails(request.form["stockname"].upper())
            if len(d) is 0:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("dashboard"))
            data = Holdings(
                orderid=request.form["orderid"],
                stockname=request.form["stockname"],
                quantity=request.form["quantity"],
                date=datetime.strptime(request.form["date"], "%d/%m/%Y").date(),
                buyingprice=request.form["buyingprice"],
                panid=session["panid"],
                cmp=d.get("cmp", 0.0),
            )
            db.session.add(data)
            db.session.commit()
            flash("Record was successfully added")
            return redirect(url_for("dashboard"))

        elif request.form["btn"] == "edit":
            d = companydetails(request.form["stockname"].upper())
            if len(d) is 0:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("dashboard"))
            rec = Holdings.query.filter_by(orderid=request.form["orderid"]).first()
            if rec is None:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("dashboard"))
            rec.stockname = request.form["stockname"]
            rec.quantity = request.form["quantity"]
            rec.date = datetime.strptime(request.form["date"], "%d/%m/%Y").date()
            rec.buyingprice = request.form["buyingprice"]
            rec.cmp = d.get("cmp", 0.0)
            db.session.add(rec)
            db.session.commit()
            flash("Record was successfully updated")
            return redirect(url_for("dashboard"))

        elif request.form["btn"] == "delete":
            rec = Holdings.query.filter_by(orderid=request.form["orderid"]).first()
            if rec is None:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("dashboard"))
            db.session.delete(rec)
            db.session.commit()
            flash("Record was successfully deleted")
            return redirect(url_for("dashboard"))
    records = Holdings.query.filter_by(panid=session["panid"]).all()
    for rec in records:
        d = companydetails(rec.stockname.upper())
        rec.cmp = d.get("cmp", 0.0)
        db.session.add(rec)
        db.session.commit()
    records = Holdings.query.filter_by(panid=session["panid"]).all()
    if not session['sentmail']:
        msg = Message('Auto Notification', sender = 'tradecasttester@gmail.com', recipients = ['shaunak.halbe@gmail.com','akshaykulkarni.0606@gmail.com'])
        msg.body = "The following stocks have risen since you bought them:\n"
        for rec in records:    
            if rec.cmp > rec.buyingprice:    
                msg.body += f"{rec.stockname} : {rec.cmp}\n"
        mail.send(msg)
        session['sentmail'] = 1
    form = holdingForm()
    form2 = deleteholdingForm()
    return render_template("index.html", form=form, data=records, form2=form2)


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
    session['sentmail'] = 0
    return redirect(url_for("login"))


@app.route("/chart.html")
def charts():
    return render_template("chart.html")


@app.route("/watchCharts.html")
def watchlistCharts():
    pricedata = []
    mystocks = Watchlist.query.filter_by(panid=session["panid"]).all()

    for x in mystocks:
        pricedata.append(get_chartdata(x.stockname, 1 / 4))

    return render_template("watchCharts.html", mystocks=pricedata, data=mystocks)


@app.route("/card.html")
def news():
    a = dict()
    records = Watchlist.query.filter_by(panid=session["panid"]).all()
    for x in records:
        a[f"{x.stockname}"] = companynews(x.stockname)
    # print(a)
    return render_template("card.html", records=records, a=a)


@app.route("/sentiment.html")
def sentiment():
    a = dict()
    records = Watchlist.query.filter_by(panid=session["panid"]).all()
    news_list = []
    for x in records:
        news_list.append(companynews(x.stockname))
    flat = [j for sub in news_list for j in sub]
    sentiment_list = get_sentiment(flat)
    for i, x in enumerate(records):
        a[f"{x.stockname}"] = sentiment_list[i]
    return render_template("sentiment.html", records=records, a=a)


@app.route("/table.html", methods=["GET", "POST"])
def watchlist():
    if (
        session.get("logged_in") is None
        or session.get("panid") is None
        or session["logged_in"] == False
    ):
        return redirect(url_for("login"))
    if request.method == "POST":
        if request.form["btn"] == "submit":
            d = companydetails(request.form["stockname"].upper())
            entries = Watchlist.query.filter_by(panid=session["panid"]).all()
            for e in entries:
                if e.stockname == request.form["stockname"].upper():
                    d = {}
                    break

            if len(d) is 0:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("watchlist"))
            data = Watchlist(
                stockname=request.form["stockname"].upper(),
                cmp=d.get("cmp", 0.0),
                marketcap=d.get("marketcap", 0.0),
                sector=d.get("sector", "none"),
                peratio=d.get("pe", 0.0),
                panid=session["panid"],
            )
            db.session.add(data)
            db.session.commit()
            flash("Record was successfully added")
            return redirect(url_for("watchlist"))
        elif request.form["btn"] == "delete":
            rec = Watchlist.query.filter_by(
                stockname=request.form["stockname"].upper()
            ).first()
            if rec is None:
                flash("Entered Details could not be fetched !")
                return redirect(url_for("watchlist"))
            db.session.delete(rec)
            db.session.commit()
            flash("Record was successfully deleted")
            return redirect(url_for("watchlist"))
    records = Watchlist.query.filter_by(panid=session["panid"]).all()
    for rec in records:
        d = companydetails(rec.stockname.upper())
        rec.cmp = d.get("cmp", 0.0)
        rec.marketcap = d.get("marketcap", 0.0)
        rec.peratio = d.get("pe", 0.0)
        db.session.add(rec)
        db.session.commit()
    records = Watchlist.query.filter_by(panid=session["panid"]).all()
    form = watchlistForm()
    return render_template("table.html", form=form, data=records)


if __name__ == "__main__":
    app.run(debug=True)
