#!flask/bin/python3
from app import app, scheduler
import app.relaycontroller as RelayController

if __name__ == '__main__':
    try:
        # Setup relays
        RelayController.setupRelays()
        RelayController.resumeState()
        # Start scheduler
        scheduler.start()
        # Run app
        app.run(debug=True,host='0.0.0.0')
    finally:
        # Reset GPIO
        RelayController.cleanup()
        # Stop scheduler
        scheduler.shutdown(wait=False)
