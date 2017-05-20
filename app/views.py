from app import app, db, login_manager, scheduler
from flask import render_template, flash, redirect, url_for, request, json
from flask_login import login_required, login_user, logout_user, current_user

from urllib.parse import urlparse, urljoin

from .models import Relay, User, RelayScenario
from .forms import LoginForm

from app import relaycontroller as RelayController

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scheduler')
@login_required
def sched():
    s = scheduler.get_jobs()
    return render_template('scheduler.html', scheduler=s)

################################################################################
# Relays
################################################################################
@app.route('/relays')
@login_required
def relays():
    r = Relay.query.all()
    return render_template('relays.html', r=r)

@app.route('/relays/changestate', methods=['POST'])
@login_required
def change_state():
    id = request.form['relayID']
    app.logger.debug('Passed RelayID: ' + str(id))

    relay = Relay.query.get(id)
    if relay:
        app.logger.debug('Changing RelayState using AJAX. Relay ID: ' + str(relay.RelayID) + ' Current relay state: ' + str(relay.State))
        if relay.State:
            app.logger.debug('Turning relay OFF...')
            result = RelayController.relayOff(relay)
        else:
            app.logger.debug('Turning relay ON...')
            result = RelayController.relayOn(relay)
    else:
        result = False

    app.logger.debug('Result: {}; RelayState: {}'.format(result, relay.State))

    if result and relay.State:
        return json.dumps({'ID' : 'relayID=' + str(relay.RelayID), 'relayStateText' : 'On'})
    elif result and not(relay.State):
        return json.dumps({'ID' : 'relayID=' + str(relay.RelayID), 'relayStateText' : 'Off'})
    else:
        return json.dumps({'ID' : 'relayID=' + str(id), 'error' : 'State change failed!'})

################################################################################
# RelayScenario
################################################################################
@app.route('/relayscenario')
@login_required
def relay_scenario():
    scenarios = RelayScenario.query.all()

    return render_template('relayscenario.html', scenarios=scenarios)

@app.route('/relayscenario/activate', methods=['POST'])
@login_required
def activate_relay_scenario():
    id = request.form['relayScenarioID']
    app.logger.debug('Passed RelayScenarioID: {}'.format(id))

    scenario = RelayScenario.query.get(id)
    if scenario:
        app.logger.debug('Activating RelayScenario using AJAX. RelayScenarioID: {}'.format(scenario.RelayScenarioID))
        result = RelayController.activateScenario(scenario)
        app.logger.debug('Result: {}'.format(result))
    else:
        result = False

    # Send JSON back to browser
    if result:
        return json.dumps({'ID' : 'relayScenarioID=' + str(scenario.RelayScenarioID), 'activationText' : 'Activated!'})
    else:
        return json.dumps({'ID' : 'relayScenarioID=' + str(id), 'error' : 'Activating scenario failed!'})

################################################################################
# Login functionality
################################################################################
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(user_id):
    return User()

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        if user.password == form.password.data:
            login_user(user, remember=True)
            flash('Login succesful!')

            next = request.args.get('next')
            app.logger.debug('Redirection target after login: ' + str(next))
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('index'))
        else:
            flash('Password incorrect!')
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for('index'))
