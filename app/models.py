from app import app, db
from flask_login import UserMixin

class RelayGroup(db.Model):
    # Database model
    RelayGroupID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True)
    Relays = db.relationship('Relay', backref='RelayGroup', lazy='dynamic')

    def __repr__(self):
        return '<RelayGroup {} - {}>'.format(self.id, self.name)


class Relay(db.Model):
        # Database model
        RelayID = db.Column(db.Integer, primary_key=True)
        Name = db.Column(db.String(50), unique=True)
        Pin = db.Column(db.Integer, nullable=True, unique=True)
        Connection = db.Column(db.String(2))
        State = db.Column(db.Boolean, nullable=True)
        RelayGroupID = db.Column(db.Integer, db.ForeignKey('RelayGroup.id'))

        def __repr__(self):
            return '<Relay {} - {}>'.format(self.id, self.name)


class RelayScenario(db.Model):
    # Database model
    RelayScenarioID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<RelayScenario {} - {}, {}>'.format(self.RelayScenarioID, self.Name)


class RelayScenarioSetup(db.Model):
    RelayScenarioID = db.Column(db.Integer, primary_key=True, db.ForeignKey('RelayScenario.RelayScenarioID'))
    RelayID = db.Column(db.Integer, db.ForeignKey('Relay.RelayID'))
    State = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return '<RelayScenarioSetup {} - {}, {}'.format(self.RelayScenarioID, self.RelayID, self.State)


class User(UserMixin):

    def __init__(self):
        self.id = 1
        self.name = 'admin'
        self.password = app.config['LOGIN_PASSWORD']
