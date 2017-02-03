from app import db

class diamonds(db.Model):
    diamond_id = db.Column(db.Integer, primary_key=True)
    carat = db.Column(db.Float)
    cut = db.Column(db.String(9))
    color = db.Column(db.String(1))
    clarity = db.Column(db.String(4))
    depth = db.Column(db.Float)
    table = db.Column(db.Float)
    price = db.Column(db.Integer)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)

    def __repr__(self):
        return '<diamond %s>' % self.diamond_id