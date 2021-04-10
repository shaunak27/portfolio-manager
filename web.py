from flask import Flask, redirect, url_for, render_template,request,flash,session
from forms import LoginForm, RegForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myproj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manager.sqlite3'
db = SQLAlchemy(app)
from models import *
@app.route("/login.html",methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        user = Investor.query.filter_by(panid=request.form['panid'],password = request.form['password']).first()
        print('hello',user)
        if user:
            session['logged_in'] = True
            session['username'] = user.username
            print('hello',user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login details are Incorrect !')
            return redirect(url_for('login'))
    form = LoginForm()
    return render_template("login.html",form=form)

@app.route("/index.html")
def dashboard():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/")
def home():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/register.html", methods=["GET","POST"])
def registration():
    if request.method == 'POST':
        user = Investor(panid = request.form['panid'],username = request.form['username'] , \
        email = request.form['email'], \
        password = request.form['password'])
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        session['username'] = user.username
        flash('Record was successfully added')
        return redirect(url_for('dashboard'))
    form = RegForm()
    return render_template("register.html",form=form)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session['logged_in'] = False
   return redirect(url_for('login'))

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
