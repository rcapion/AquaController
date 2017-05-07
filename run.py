#!flask/bin/python
from app import app
import app.relaycontroller as RelayController
if __name__ == '__main__':
    try:
        # Setup relays
        RelayController.setupRelays()
        RelayController.resumeState()
        # Run app
        app.run(debug=True,host='0.0.0.0')
    finally:
        # Reset GPIO
        RelayController.cleanup()
