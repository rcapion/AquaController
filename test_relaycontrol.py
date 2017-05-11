#!flask/bin/python3
from app import app, db
import app.relaycontroller as RelayController
from app.models import *
from time import sleep


print('*****************************************************')
print('**  Testing setupRelays, resumeState               **')
print('*****************************************************')

RelayController.setupRelays()

RelayController.resumeState()

print('*****************************************************')
print('**  Testing relayOn, relayOff                      **')
print('*****************************************************')

r=Relay()

sleep(2)
RelayController.relayOn(r.query.get(1))
sleep(2)
RelayController.relayOff(r.query.get(1))
sleep(1)
RelayController.relayOn(r.query.get(2))
sleep(2)
RelayController.relayOff(r.query.get(2))
sleep(5)

print('*****************************************************')
print('**  Testing activateScenario                       **')
print('*****************************************************')

s1 = RelayScenario.query.get(1)
s2 = RelayScenario.query.get(2)

RelayController.activateScenario(s1, False)
sleep(2)
RelayController.activateScenario(s2, False)
sleep(2)
RelayController.activateScenario(s1)
sleep(2)
RelayController.activateScenario(s2)
sleep(5)

print('*****************************************************')
print('**  Testing cleanup                                **')
print('*****************************************************')

RelayController.cleanup()
