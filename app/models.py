from app import db
from flask_login import UserMixin

class RelayGroups(db.Model):
    # Database model
    __tablename__ = 'relaygroups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    relays = db.relationship('Relay', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Group {} - {}>'.format(self.id, self.name)


class Relay(db.Model):
        # Database model
        __tablename__ = 'relay'
        id         = db.Column(db.Integer, primary_key=True)
        name       = db.Column(db.String(50), unique=True)
        pin        = db.Column(db.Integer, nullable=True, unique=True)
        connection = db.Column(db.String(2))
        state      = db.Column(db.Boolean, nullable=True)
        group_id = db.Column(db.Integer, db.ForeignKey('relaygroups.id'))

        def __repr__(self):
            return '<Relay {} - {}>'.format(self.id, self.name)

        # def __init__(self):
        #     # Parse configfile
        #     self.config = configparser.ConfigParser()
        #     self.config.read('RelaySetup.ini')

class User(UserMixin):

    def __init__(self):
        self.id = 1
        self.name = 'admin'
        self.password = 'password'
