import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Debugging
DEBUG = True
DEBUG_TOOLBAR = False
DEBUG_TB_INTERCEPT_REDIRECTS = True

SECRET_KEY = 'DenHemmeligeHemmeligeKode'

# SQLite DB setup
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'AquaController.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
