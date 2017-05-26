import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler


###############################################################################
# Instantiate app
app = Flask(__name__)
app.config.from_object('config')

###############################################################################
# Instantiate db
db = SQLAlchemy(app)
# Activate ForeignKey support for SQLite DB
# http://www.eqianli.tech/questions/5124094/sqlite-pragma-foreign-keys-with-sqlalchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

###############################################################################
# Instantiate login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

###############################################################################
# Setup DebugToolbar
if app.config['DEBUG_TOOLBAR']:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)

###############################################################################
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

###############################################################################
if not os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    # Instantiate scheduler
    scheduler = BackgroundScheduler({
        'apscheduler.jobstores.default': {
            'type': 'sqlalchemy',
            'url': app.config['SQLALCHEMY_DATABASE_URI']
        },
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.job_defaults': {
            'coalesce': 'true',
            'max_instances': '1',
            'misfire_grace_time': '59'
        },
        'apscheduler.logger': app.logger
    })

###############################################################################
# Import rest of app
from app import views, models
