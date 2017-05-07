from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instantiate app
app = Flask(__name__)
app.config.from_object('config')
# Instantiate db
db = SQLAlchemy(app)
# Instantiate login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Activate ForeignKey for SQLite DB
# http://www.eqianli.tech/questions/5124094/sqlite-pragma-foreign-keys-with-sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Setup DebugToolbar
if app.config['DEBUG_TOOLBAR']:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)

# Setup logging
import logging
from logging.handlers import RotatingFileHandler
# File handler
file_handler = RotatingFileHandler('tmp/AquaController.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(file_handler)
# Set log level
if app.debug:
    app.logger.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
else:
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

app.logger.info('AquaController startup')

# Import rest of app
from app import views, models
