from db import db 


class LogisticModel(db.Model):

    __tablename__ = "logistic_model"

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(20))
    feature = db.Column(db.String(120))
    coef = db.Column(db.Float())

    def __init__(self, version, feature, coef):
        self.version = version
        self.feature = feature
        self.coef = coef 

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()
