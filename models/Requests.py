from db import db 


class Requests(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dt = db.Column(db.DateTime)

    def __init__(self, user_id, dt):
        self.user_id = user_id 
        self.dt = dt 

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class RequestsInfo(db.Model):
    __tablename__ = 'requests_info'

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
    model_version = db.Column(db.String)
    feature = db.Column(db.Text)
    value = db.Column(db.Float) 

    def __init__(self, request_id, model_version, feature, value):
        self.request_id = request_id
        self.model_version = model_version
        self.feature = feature 
        self.value = value 
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()