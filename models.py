from web import db


class Investor(db.Model):
    panid = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(30))
    password = db.Column(db.String(15))
    # mobileno = db.Column(db.String(10))

    def __init__(self, panid, username, email, password):
        self.panid = panid
        self.username = username
        self.email = email
        self.password = password


class Holdings(db.Model):
    orderid = db.Column(db.Integer, primary_key=True)
    stockname = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)
    buyingprice = db.Column(db.Integer)

    def __init__(self, orderid, stockname, quantity, buyingprice, date):
        self.orderid = orderid
        self.stockname = stockname
        self.quantity = quantity
        self.buyingprice = buyingprice
        self.date = date