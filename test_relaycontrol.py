#!flask/bin/python
from app import app, db
import app.relaycontroller as RelayController
from app.models import Relay
from time import sleep

RelayController.setupRelays()

RelayController.resumeState()

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

RelayController.cleanup()
