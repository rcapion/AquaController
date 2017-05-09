from app import app, db
from app.models import Relay
import RPi.GPIO as GPIO
from time import sleep
# Valid BCM GPIO pin numbers on Raspberry Pi
valid_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

def setupRelays():
    '''Reads and sets up the corresponding pins as outputs'''
    # Set GPIO naming scheme to BCM
    GPIO.setmode(GPIO.BCM)

    # Going through all relays and setting them up
    _relays = Relay.query.all()
    for relay in _relays:
        # Testing for valid pin and setting pin as output
        if isinstance(relay.Pin, int) and relay.Pin in valid_pins:
            app.logger.info('Setting up GPIO pin ' + str(relay.Pin) + ' for relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\'')
            GPIO.setup(relay.Pin, GPIO.OUT, initial=GPIO.HIGH)
        else:
            app.logger.error('Unable to setup GPIO pin - pin number \'' + str(relay.Pin) + '\' not valid!')

def resumeState():
    '''Sets all relays to last known state'''
    # Go through all relays and get last state and set accordingly
    _relays = Relay.query.all()
    for relay in _relays:
        app.logger.info('Turning relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' ' + ('ON' if relay.State else 'OFF'))
        setState(relay, relay.State)
        app.logger.debug('Sleeping...')
        sleep(1)
def cleanup():
    '''Cleans up GPIO pins and resets them to input'''
    app.logger.info('Cleaning up GPIO')
    GPIO.cleanup()

def setState(relay, state):
    if relay.Pin in valid_pins:
        if (state and relay.Connection == 'NO') or (not state and relay.Connection == 'NC'):
            app.logger.debug('Setting output to GPIO.LOW, because state=' + str(state) + ' and connection=' + relay.Connection)
            try:
                GPIO.output(relay.Pin, GPIO.LOW)
                app.logger.info('Relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' turned ' + ('ON' if state else 'OFF'))
                return True
            except:
               app.logger.error('Unexpected error when setting GPIO.output')
               return False

        elif (state and relay.Connection == 'NC') or (not state and relay.Connection == 'NO'):
            app.logger.debug('Setting output to GPIO.HIGH, because state=' + str(state) + ' and connection=' + relay.Connection)
            try:
                GPIO.output(relay.Pin, GPIO.HIGH)
                app.logger.info('Relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' turned ' + ('ON' if state else 'OFF'))
                return True
            except:
               app.logger.error('Unexpected error when setting GPIO.output')
               return False

        else:
            app.logger.error('Unable to set state for relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' because connection type \'' + relay.Connection + '\' is unknown')
            return False
    else:
        app.logger.error('Unable to set state for relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' because of invalid GPIO pin')
        return False


def relayOn(relays):
    if hasattr(relays, '__iter__'):
        for relay in relays:
            app.logger.info('Turning relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' ' + 'ON')
            result = setState(relay, True)
            app.logger.info('Saving state for relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' ')
            relay.State = True
            db.session.commit()
            app.logger.debug('State saved')
    else:
        app.logger.info('Turning relay ' + str(relays.RelayID) + ' \'' + relays.Name + '\' ' + 'ON')
        result = setState(relays, True)
        app.logger.info('Saving state for relay ' + str(relays.RelayID) + ' \'' + relays.Name + '\' ')
        relays.State = True
        db.session.commit()
        app.logger.debug('State saved')

    return result

def relayOff(relays):
    if hasattr(relays, '__iter__'):
        for relay in relays:
            app.logger.info('Turning relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' ' + 'OFF')
            result = setState(relay, False)
            app.logger.debug('Saving state for relay ' + str(relay.RelayID) + ' \'' + relay.Name + '\' ')
            relay.State = False
            db.session.commit()
            app.logger.debug('State saved')
    else:
        app.logger.info('Turning relay ' + str(relays.RelayID) + ' \'' + relays.Name + '\' ' + 'OFF')
        result = setState(relays, False)
        app.logger.info('Saving state for relay ' + str(relays.RelayID) + ' \'' + relays.Name + '\' ')
        relays.State = False
        db.session.commit()
        app.logger.debug('State saved')

    return result

def relayGroupOn(self, group_name):
    pass

def relayGroupOff(self, group_name):
    pass
