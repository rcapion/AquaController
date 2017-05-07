from app import app, db
from app.models import Relay
import RPi.GPIO as GPIO
from time import sleep

class RelayController():
    '''Relay controller using GPIO on RaspberryPi'''
    # Valid BCM GPIO pin numbers on Raspberry Pi
    valid_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

    @classmethod
    def setupRelays(cls):
        '''Reads and sets up the corresponding pins as outputs'''
        # Set GPIO naming scheme to BCM
        GPIO.setmode(GPIO.BCM)

        # Going through all relays and setting them up
        _relays = Relay()
        for relay in _relays.query.all():
            # Testing for valid pin and setting pin as output
            if isinstance(relay.pin, int) and relay.pin in cls.valid_pins:
                app.logger.info('Setting up GPIO pin ' + str(relay.pin) + ' for relay ' + str(relay.id) + ' \'' + relay.name + '\'')
                GPIO.setup(relay.pin, GPIO.OUT, initial=GPIO.HIGH)
            else:
                app.logger.error('Unable to setup GPIO pin - pin number \'' + str(relay.pin) + '\' not valid!')

    @classmethod
    def resumeState(cls):
        '''Sets all relays to last known state'''
        # Go through all relays and get last state and set accordingly
        _relays = Relay()
        for relay in _relays.query.all():
            app.logger.info('Turning relay ' + str(relay.id) + ' \'' + relay.name + '\' ' + 'ON' if relay.state else 'OFF')
            cls.setState(relay, relay.state)

    @classmethod
    def cleanup(cls):
        '''Cleans up GPIO pins and resets them to input'''
        app.logger.info('Cleaning up GPIO')
        GPIO.cleanup()

    @classmethod
    def setState(cls, relay, state):
        if relay.pin in RelayController.valid_pins:
            if (state and relay.connection == 'NO') or (not state and relay.connection == 'NC'):
                app.logger.debug('Setting output to GPIO.LOW, because state: ' + str(state) + ' and connection: ' + relay.connection)
                #try:
                GPIO.output(relay.pin, GPIO.LOW)
                app.logger.info('Relay ' + str(relay.id) + ' \'' + relay.name + '\' turned ' + 'ON' if state else 'OFF')
                #except:
                #    app.logger.error('Unexpected error when setting GPIO.output')

            elif (state and relay.connection == 'NC') or (not state and relay.connection == 'NO'):
                app.logger.debug('Setting output to GPIO.HIGH, because state: ' + str(state) + ' and connection: ' + relay.connection)
                #try:
                GPIO.output(relay.pin, GPIO.HIGH)
                app.logger.info('Relay ' + str(relay.id) + ' \'' + relay.name + '\' turned ' + 'ON' if state else 'OFF')
                #except:
                #    app.logger.error('Unexpected error when setting GPIO.output')

            else:
                app.logger.error('Unable to set state for relay ' + str(relay.id) + ' \'' + relay.name + '\' because connection type \'' + relay.connection + '\' is unknown')
        else:
            app.logger.error('Unable to set state for relay ' + str(relay.id) + ' \'' + relay.name + '\' because of invalid GPIO pin')

    @classmethod
    def relayOn(cls, relays):
        if hasattr(relays, '__iter__'):
            for relay in relays:
                app.logger.info('Turning relay ' + str(relay.id) + ' \'' + relay.name + '\' ' + 'ON')
                RelayController.setState(relay, True)
                app.logger.info('Saving state for relay ' + str(relay.id) + ' \'' + relay.name + '\' ')
                relay.state = True
                db.session.commit()
                app.logger.info('State saved')
        else:
            app.logger.info('Turning relay ' + str(relay.id) + ' \'' + relay.name + '\' ' + 'ON')
            RelayController.setState(relays, True)
            app.logger.info('Saving state for relay ' + str(relay.id) + ' \'' + relay.name + '\' ')
            relay.state = True
            db.session.commit()
            app.logger.info('State saved')

    @classmethod
    def relayOff(cls, relays):
        if hasattr(relays, '__iter__'):
            for relay in relays:
                app.logger.info('Turning relay ' + str(relay.id) + ' \'' + relay.name + '\' ' + 'OFF')
                RelayController.setState(relay, False)
                app.logger.info('Saving state for relay ' + str(relay.id) + ' \'' + relay.name + '\' ')
                relay.state = False
                db.session.commit()
                app.logger.info('State saved')
                sleep(1)
        else:
            app.logger.info('Turning relay ' + str(relay.id) + ' \'' + relay.name + '\' ' + 'OFF')
            RelayController.setState(relays, False)
            app.logger.info('Saving state for relay ' + str(relay.id) + ' \'' + relay.name + '\' ')
            relay.state = False
            db.session.commit()
            app.logger.info('State saved')

    def relayGroupOn(self, group_name):
        pass

    def relayGroupOff(self, group_name):
        pass
