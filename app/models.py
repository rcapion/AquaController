from app import app, db
from flask_login import UserMixin

class RelayGroup(db.Model):
    # Database model
    __tablename__ = 'relaygroup'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    relays = db.relationship('Relay', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<RelayGroup {} - {}>'.format(self.id, self.name)


class Relay(db.Model):
        # Database model
        __tablename__ = 'relay'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), unique=True)
        pin = db.Column(db.Integer, nullable=True, unique=True)
        connection = db.Column(db.String(2))
        state = db.Column(db.Boolean, nullable=True)
        group_id = db.Column(db.Integer, db.ForeignKey('relaygroups.id'))

        def __repr__(self):
            return '<Relay {} - {}>'.format(self.id, self.name)

class RelayScenario(db.Model):
    # Database model
    __tablename__ = 'relayscenario'
    id = db.Column(db.Integer)
    relay_id = db.Column(db.Integer, db.ForeignKey('relay.id'))
    state = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return '<RelayScenario {} - {}, {}>'.format(self.id, self.relay_id, self.state)

class User(UserMixin):

    def __init__(self):
        self.id = 1
        self.name = 'admin'
        self.password = app.config['LOGIN_PASSWORD']
