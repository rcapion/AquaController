import os
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# Login password
LOGIN_PASSWORD = 'Test'

# Debugging
DEBUG = True
DEBUG_TOOLBAR = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

SECRET_KEY = 'DenHemmeligeHemmeligeKode'

# SQLite DB setup
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'AquaController.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Valid BCM GPIO pin numbers on Raspberry Pi
VALID_GPIO_PINS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
# Time interval between several relays are turned on
RELAY_SLEEP_TIME = 0.5

# # APScheduler setup
# SCHEDULER_JOBSTORES = {
#     'default': SQLAlchemyJobStore(url='sqlite:///' + os.path.join(basedir, 'AquaController_Scheduler.db'))
# }
# SCHEDULER_API_ENABLED = True
# SCHEDULER_EXECUTORS = {
#     'default': {'type': 'threadpool', 'max_workers': 20}
# }
# SCHEDULER_JOB_DEFAULTS = {
#     'coalesce': False,
#     'max_instances': 3
# }
# # Test job
# # JOBS = [
# #     {
# #         'id': 'job1',
# #         'func': 'app:job1',
# #         'args': (1, 2),
# #         'trigger': 'interval',
# #         'seconds': 10
# #     }
# # ]
