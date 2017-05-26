#!flask/bin/python3
import os
from app import app
import app.relaycontroller as RelayController

if __name__ == '__main__':

    if not os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # Start scheduler
        scheduler.start()

        # Setup relays
        RelayController.setupRelays()
        RelayController.resumeState()

    try:
        # Run app
        app.run(debug=True,host='0.0.0.0')
    finally:
        # Shut down the scheduler when exiting the app
        scheduler.shutdown(wait=False)
        # Reset GPIO when exiting the app
        RelayController.cleanup()
