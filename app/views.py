from app import app, db, login_manager
from flask import render_template, flash, redirect, url_for, request, json
from flask_login import login_required, login_user, logout_user, current_user

from urllib.parse import urlparse, urljoin

from .models import Relay, User
from .forms import LoginForm

from app import relaycontroller as RelayController

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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

    app.logger.debug('Changing state using AJAX. Relay ID: ' + str(relay.RelayID) + ' Current relay state: ' + str(relay.State))

    if relay.state:
        app.logger.debug('Turning relay OFF...')
        result = RelayController.relayOff(relay)
        app.logger.debug('Result: ' + str(result))
        if result:
            return json.dumps({'ID' : 'relayID=' + str(relay.RelayID), 'relayStateText' : 'Off'})
        else:
            return json.dumps({'ID' : 'relayID=' + str(relay.RelayID), 'error' : 'State change failed!'})
    else:
        app.logger.debug('Turning relay ON...')
        result = RelayController.relayOn(relay)
        app.logger.debug('Result: ' + str(result))
        if result:
            return json.dumps({'ID' : 'relayID=' + str(relay.RelayID), 'relayStateText' : 'On'})
        else:
            return json.dumps({'ID' : 'relayID=' + str(relay.RelayID), 'error' : 'State change failed!'})


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
