import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Login password
LOGIN_PASSWORD = 'Test'

# Debugging
DEBUG = True
DEBUG_TOOLBAR = False
DEBUG_TB_INTERCEPT_REDIRECTS = True

SECRET_KEY = 'DenHemmeligeHemmeligeKode'

# SQLite DB setup
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'AquaController.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Valid BCM GPIO pin numbers on Raspberry Pi
VALID_GPIO_PINS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
# Time interval between several relays are turned on
RELAY_SLEEP_TIME = 0.5 
