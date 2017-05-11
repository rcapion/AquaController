from app import app, db
from flask_login import UserMixin

class RelayGroup(db.Model):
    # Database model
    __tablename__ = 'RelayGroup'
    RelayGroupID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True)
    Relay = db.relationship('Relay', backref='RelayGroup', cascade='all, delete', lazy='dynamic')

    def __init__(self, Name=None):
        self.Name = Name

    def __repr__(self):
        return '<RelayGroup {} - {}>'.format(self.RelayGroupID, self.Name)


class Relay(db.Model):
        # Database model
        __tablename__ = 'Relay'
        RelayID = db.Column(db.Integer, primary_key=True)
        Name = db.Column(db.String(50), unique=True)
        Pin = db.Column(db.Integer, nullable=True, unique=True)
        Connection = db.Column(db.String(2))
        State = db.Column(db.Boolean, nullable=True)
        RelayGroupID = db.Column(db.Integer, db.ForeignKey('RelayGroup.RelayGroupID'), nullable=True)

        def __init__(self, Name=None, Pin=None, Connection=None, State=None, RelayGroupID=None):
            self.Name = Name
            self.Pin = Pin
            self.Connection = Connection
            self.State = State
            self.RelayGroupID = RelayGroupID

        def __repr__(self):
            return '<Relay {} - {}>'.format(self.RelayID, self.Name)


class RelayScenario(db.Model):
    # Database model
    __tablename__ = 'RelayScenario'
    RelayScenarioID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True)
    Setup = db.relationship('RelayScenarioSetup', backref='RelayScenario', lazy='dynamic')

    def __init__(self, Name=None):
        self.Name = Name

    def __repr__(self):
        return '<RelayScenario {} - {}>'.format(self.RelayScenarioID, self.Name)


class RelayScenarioSetup(db.Model):
    __tablename__ = 'RelayScenarioSetup'
    SetupID = db.Column(db.Integer, primary_key=True)
    RelayScenarioID = db.Column(db.Integer, db.ForeignKey('RelayScenario.RelayScenarioID'))
    RelayID = db.Column(db.Integer, db.ForeignKey('Relay.RelayID'))
    State = db.Column(db.Boolean, nullable=True)

    def __init__(self, RelayScenarioID=None, RelayID=None, State=None):
        self.RelayScenarioID = RelayScenarioID
        self.RelayID = RelayID
        self.State = State

    def __repr__(self):
        return '<RelayScenarioSetup {} - RelayScenario {}, Relay {}, State {}>'.format(self.SetupID, self.RelayScenarioID, self.RelayID, self.State)


class User(UserMixin):

    def __init__(self):
        self.id = 1
        self.name = 'admin'
        self.password = app.config['LOGIN_PASSWORD']
