#!flask/bin/python3
import os
from app import app, scheduler
import app.relaycontroller as RelayController

if __name__ == '__main__':

    # if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # Start scheduler
    scheduler.start()
    # Setup relays
    RelayController.setupRelays()
    RelayController.resumeState()

    try:
        # Run app
        app.run(debug=True,host='0.0.0.0',use_reloader=False)
    finally:
        # Shut down the scheduler when exiting the app
        scheduler.shutdown(wait=False)
        # Reset GPIO when exiting the app
        RelayController.cleanup()
