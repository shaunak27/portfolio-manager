from app import db


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

class Admin(db.Model):
    loginid = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(15))
    

    def __init__(self, loginid, email, password):
        self.loginid = loginid
        self.email = email
        self.password = password

class Holdings(db.Model):
    orderid = db.Column(db.Integer, primary_key=True)
    stockname = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)
    buyingprice = db.Column(db.Integer)
    panid = db.Column(db.String(10))
    cmp = db.Column(db.Float)
    def __init__(self, orderid, stockname, quantity, buyingprice, date,panid,cmp):
        self.orderid = orderid
        self.stockname = stockname
        self.quantity = quantity
        self.buyingprice = buyingprice
        self.date = date
        self.panid = panid
        self.cmp = cmp
class Watchlist(db.Model):
    stockname = db.Column(db.String(10),primary_key=True)
    panid = db.Column(db.String(10))
    sector = db.Column(db.String(20))
    cmp = db.Column(db.Float)
    marketcap = db.Column(db.Float)
    peratio = db.Column(db.Float)
    def __init__(self, sector, stockname, cmp, marketcap, peratio,panid):
        self.stockname = stockname
        self.panid = panid
        self.cmp = cmp
        self.marketcap = marketcap
        self.peratio = peratio
        self.sector = sector
