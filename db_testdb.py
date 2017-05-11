#!flask/bin/python3
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from app.models import *

# g1 = RelayGroup()
# g1.Name = 'Main Group'
#
# g2 = RelayGroup()
# g2.Name = 'Secondary Group'
#
# db.session.add(g1)
# db.session.add(g2)
# db.session.commit()
#
# r1 = Relay()
# r1.Name = 'Relay01'
# r1.Pin = 26
# r1.Connection = 'NC'
# r1.State = True
# r1.RelayGroupID = 1
#
# r2 = Relay()
# r2.Name = 'Relay02'
# r2.Pin = 19
# r2.Connection = 'NO'
# r2.State = True
# r2.RelayGroupID = 1
#
# r3 = Relay()
# r3.Name = 'Relay03'
# r3.Pin = 13
# r3.Connection = ''
# r3.State = False
# r3.RelayGroupID = 1
#
# r4 = Relay()
# r4.Name = 'Relay04'
# r4.Connection = 'NO'
# r4.State = True
# r4.RelayGroupID = 2
#
# db.session.add(r1)
# db.session.add(r2)
# db.session.add(r3)
# db.session.add(r4)
# db.session.commit()
#
# s1 = RelayScenario()
# s1.Name = 'Test1'
#
# s2 = RelayScenario()
# s2.Name = 'Test2'
#
# db.session.add(s1)
# db.session.add(s2)
# db.session.commit()

ss = [
    RelayScenarioSetup(1,1,True),
    RelayScenarioSetup(1,2,True),
    RelayScenarioSetup(1,3,True),
    RelayScenarioSetup(2,1,False),
    RelayScenarioSetup(2,2,False),
    RelayScenarioSetup(2,3,False)
]
db.session.bulk_save_objects(ss)
db.session.commit()
