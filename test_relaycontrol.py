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
#
# sleep(2)
# RelayController.relayOn(Relay.query.get(1))
# sleep(2)
# RelayController.relayOff(Relay.query.get(1))
# sleep(1)
# RelayController.relayOn(Relay.query.all())
# sleep(2)
# RelayController.relayOff(Relay.query.all())
# sleep(5)

r = Relay.query.get(1)
s = r.Name
t = r.RelayID
lst = [r, s, t, 'test2', 47]

print(lst)

for i in lst:
    RelayController.relayOff(i)
    RelayController.relayOn(i)

# print('*****************************************************')
# print('**  Testing activateScenario                       **')
# print('*****************************************************')
#
# s1 = RelayScenario.query.get(1)
# s2 = RelayScenario.query.get(2)
#
# RelayController.activateScenario(s1, False)
# sleep(2)
# RelayController.activateScenario(s2, False)
# sleep(2)
# RelayController.activateScenario(s1)
# sleep(2)
# RelayController.activateScenario(s2)
# sleep(5)
#
# a=RelayScenario.query.get(1)
# b=a.Name
# c=a.RelayScenarioID
# lst = [a, b, c, 'test', 324]
#
# for i in lst:
#     RelayController.activateScenario(i)

print('*****************************************************')
print('**  Testing cleanup                                **')
print('*****************************************************')

RelayController.cleanup()
