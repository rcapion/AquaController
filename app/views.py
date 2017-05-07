from app import app, db, login_manager
from flask import render_template, flash, redirect, url_for, request, json
from flask_login import login_required, login_user, logout_user, current_user

from urllib.parse import urlparse, urljoin

from .models import Relay, User
from .forms import LoginForm

from app import relaycontroller as RelayController

@app.route('/')
@app.route('/index')
@login_required
def index():
    return "Hello, World!"

@app.route('/relays')
@login_required
def relays():
    r = Relay()
    return render_template('relays.html', r=r.query.all())

@app.route('/relays/changestate', methods=['POST'])
@login_required
def changestate():
    request.form
    id = request.form['relayID']

    relay = Relay.query.get(id)

    app.logger.debug('Changing state using AJAX. Relay ID: ' + str(relay.id) + ' Current relay state: ' + str(relay.state))

    if relay.state:
        app.logger.debug('Turning relay OFF...')
        result = RelayController.relayOff(relay)
        app.logger.debug('Result: ' + str(result))
        if result:
            return json.dumps({'ID' : 'relayID=' + str(relay.id), 'relayStateText' : 'Off'})
        else:
            return json.dumps({'ID' : 'relayID=' + str(relay.id), 'error' : 'State change failed!'})
    else:
        app.logger.debug('Turning relay ON...')
        result = RelayController.relayOn(relay)
        app.logger.debug('Result: ' + str(result))
        if result:
            return json.dumps({'ID' : 'relayID=' + str(relay.id), 'relayStateText' : 'On'})
        else:
            return json.dumps({'ID' : 'relayID=' + str(relay.id), 'error' : 'State change failed!'})

@app.route('/relay/on/<id>')
def relay_on(id):
    try:
        id = int(id)
        r = Relay()
        RelayController.relayOn(r.query.get(id))
        return redirect(url_for('relays'))
    except TypeError:
        abort(400)

@app.route('/relay/off/<id>')
def relay_off(id):
    try:
        id = int(id)
        r = Relay()
        RelayController.relayOff(r.query.get(id))
        return redirect(url_for('relays'))
    except TypeError:
        abort(400)

# Login functionality
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

            next = request.args.get('next')
            app.logger.debug('Redirection target after login: ' + str(next))
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('index'))
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for('index'))
