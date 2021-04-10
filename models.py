from web import db

class Investor(db.Model):
    panid = db.Column(db.String(10), primary_key = True)
    username = db.Column( db.String(20))
    email = db.Column(db.String(30))
    password = db.Column(db.String(15))  
    #mobileno = db.Column(db.String(10))

def __init__(self, panid,username, email, password):
    self.panid = panid
    self.username = username
    self.email = email
    self.password = password
    
