from app import app, db
from app.models import Relay, RelayScenario
import RPi.GPIO as GPIO
from time import sleep

# Valid BCM GPIO pin numbers on Raspberry Pi
valid_pins = app.config['VALID_GPIO_PINS']
app.logger.debug('Valid GPIO pins: {}'.format(valid_pins))

def setupRelays():
    '''Reads and sets up the corresponding pins as outputs'''

    # Set GPIO naming scheme to BCM
    GPIO.setmode(GPIO.BCM)

    # Going through all relays and setting them up
    relays = Relay.query.all()
    for relay in relays:
        # Testing for valid pin and setting pin as output
        if relay.Pin in valid_pins:
            app.logger.info('Setting up GPIO pin {} for relay {} \'{}\''.format(relay.Pin, relay.RelayID, relay.Name))
            GPIO.setup(relay.Pin, GPIO.OUT, initial=GPIO.HIGH)
        else:
            app.logger.error('Unable to setup GPIO pin - pin number \'{}\' not valid!'.format(relay.Pin))

def resumeState():
    '''Sets all relays to last known state'''

    app.logger.info('Resuming last known state of all relays')

    # Go through all relays and get last state and set accordingly
    relays = Relay.query.all()
    length = len(relays)
    for i, relay in enumerate(relays):
        app.logger.info('Turning relay {} \'{}\' {}'.format(relay.RelayID, relay.Name, 'ON' if relay.State else 'OFF'))
        setState(relay, relay.State)
        if i != length-1:
            app.logger.debug('Waiting before next relay is being set')
            sleep(app.config['RELAY_SLEEP_TIME'])

def cleanup():
    '''Cleans up GPIO pins and resets them to input'''

    app.logger.info('Cleaning up GPIO')
    GPIO.cleanup()
def processRelayArg(relay_arg):
    if isinstance(relay_arg, str):
        relays = Relay.query.filter_by(Name=relay_arg).first()
        app.logger.debug('Input argument \'{}\' converted to {}'.format(relay_arg, relays))
    elif isinstance(relay_arg, int):
        relays = Relay.query.get(relay_arg)
        app.logger.debug('Input argument \'{}\' converted to {}'.format(relay_arg, relays))
    elif isinstance(relay_arg, object):
        relays = relay_arg
        app.logger.debug('Input argument {} not converted'.format(relays))
    else:
        app.logger.error('Input argument is of unknown type')
        return None

    return relays

def setState(relay_arg, state):
    '''Sets/changes state of relay'''
    # Tests arguments
    relay = processRelayArg(relay_arg)
    if relay == None:
        app.logger.error('Not possible to query Relay based on passed argument  \'{}\''.format(relay_arg))
        return False

    if relay.Pin in valid_pins:
        if (state and relay.Connection == 'NO') or (not state and relay.Connection == 'NC'):
            app.logger.debug('Setting output to GPIO.LOW, because state={} and connection={}'.format(state, relay.Connection))
            try:
                GPIO.output(relay.Pin, GPIO.LOW)
                app.logger.debug('Relay {} \'{}\' turned {}'.format(relay.RelayID, relay.Name, 'ON' if state else 'OFF'))
                return True
            except:
                app.logger.error('Unexpected error when setting GPIO.output')
                return False

        elif (state and relay.Connection == 'NC') or (not state and relay.Connection == 'NO'):
            app.logger.debug('Setting output to GPIO.HIGH, because state={} and connection={}'.format(state, relay.Connection))
            try:
                GPIO.output(relay.Pin, GPIO.HIGH)
                app.logger.debug('Relay {} \'{}\' turned {}'.format(relay.RelayID, relay.Name, 'ON' if state else 'OFF'))
                return True
            except:
                app.logger.error('Unexpected error when setting GPIO.output')
                return False

        else:
            app.logger.error('Unable to set state for relay {} \'{}\' because connection type \'{}\' is unknown'.format(relay.RelayID, relay.Name, relay.Connection))
            return False
    else:
        app.logger.error('Unable to set state for relay {} \'{}\' because of invalid GPIO pin'.format(relay.RelayID, relay.Name))
        return False


def relayOn(relay_arg):
    # Tests arguments
    relays = processRelayArg(relay_arg)
    if relays == None:
        app.logger.error('Not possible to query Relay based on passed argument  \'{}\''.format(relay_arg))
        return False

    # Go trough relays and turn them on
    if hasattr(relays, '__iter__'):
        length = len(relays)
        for i, relay in enumerate(relays):
            app.logger.info('Turning relay {} \'{}\' ON'.format(relay.RelayID, relay.Name))
            result = setState(relay, True)
            app.logger.info('Saving state for relay {} \'{}\''.format(relay.RelayID, relay.Name))
            relay.State = True
            db.session.commit()
            app.logger.debug('State saved')
            if i != length-1:
                app.logger.debug('Waiting before next relay is being set')
                sleep(app.config['RELAY_SLEEP_TIME'])
    else:
        app.logger.info('Turning relay {} \'{}\' ON'.format(relays.RelayID, relays.Name))
        result = setState(relays, True)
        app.logger.info('Saving state for relay {} \'{}\''.format(relays.RelayID, relays.Name))
        relays.State = True
        db.session.commit()
        app.logger.debug('State saved')

    # Return result of setState
    return result

def relayOff(relay_arg):
    # Tests arguments
    relays = processRelayArg(relay_arg)
    if relays == None:
        app.logger.error('Not possible to query Relay based on passed argument  \'{}\''.format(relay_arg))
        return False

    # Go trough relays and turn them off
    if hasattr(relays, '__iter__'):
        length = len(relays)
        for i, relay in enumerate(relays):
            app.logger.info('Turning relay {} \'{}\' OFF'.format(relay.RelayID, relay.Name))
            result = setState(relay, False)
            app.logger.info('Saving state for relay {} \'{}\''.format(relay.RelayID, relay.Name))
            relay.State = False
            db.session.commit()
            app.logger.debug('State saved')
            if i != length-1:
                app.logger.debug('Waiting before next relay is being set')
                sleep(app.config['RELAY_SLEEP_TIME'])
    else:
        app.logger.info('Turning relay {} \'{}\' OFF'.format(relays.RelayID, relays.Name))
        result = setState(relays, False)
        app.logger.info('Saving state for relay {} \'{}\''.format(relays.RelayID, relays.Name))
        relays.State = False
        db.session.commit()
        app.logger.debug('State saved')

    # Return result of setState
    return result

def relayGroupOn(self, group_name):
    pass

def relayGroupOff(self, group_name):
    pass

def activateScenario(scenario_arg, store_state=True):
    '''Activates RelayScenario'''
    # Tests arguments
    if isinstance(scenario_arg, str):
        scenario = RelayScenario.query.filter_by(Name=scenario_arg).first()
        app.logger.debug('Input argument \'{}\' converted to {}'.format(scenario_arg, scenario))
    elif isinstance(scenario_arg, int):
        scenario = RelayScenario.query.get(scenario_arg)
        app.logger.debug('Input argument \'{}\' converted to {}'.format(scenario_arg, scenario))
    elif isinstance(scenario_arg, object):
        scenario = scenario_arg
        app.logger.debug('Input argument {} not converted'.format(scenario))
    else:
        app.logger.error('Input argument is of unknown type')

    if scenario == None:
        app.logger.error('Not possible to query RelayScenario based on passed argument \'{}\''.format(scenario_arg))
        return False

    if store_state:
        app.logger.info('Activating RelayScenario {} \'{}\' and storing state'.format(scenario.RelayScenarioID, scenario.Name))
    else:
        app.logger.info('Activating RelayScenario {} \'{}\' - states are not being stored'.format(scenario.RelayScenarioID, scenario.Name))

    # Go through RelaySetups in RelayScenario
    length = len(scenario.Setup.all())
    for i, relay_setup in enumerate(scenario.Setup):
        relay = relay_setup.RelayID
        state = relay_setup.State

        if store_state:
            if state:
                relayOn(relay)
            else:
                relayOff(relay)
        else:
            setState(relay, state)

        if i != length-1:
            app.logger.debug('Sleeping...')
            sleep(app.config['RELAY_SLEEP_TIME'])

    app.logger.info('RelayScenario {} \'{}\' activated'.format(scenario.RelayScenarioID, scenario.Name))
    return True
