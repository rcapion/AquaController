from app import app, db, login_manager, scheduler
from flask import render_template, flash, redirect, url_for, request, json
from flask_login import login_required, login_user, logout_user, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NoneOf

from urllib.parse import urlparse, urljoin

from .models import Relay, User, RelayScenario, RelayScenarioSetup
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

@app.route('/relayscenario/add', methods=['GET', 'POST'])
@login_required
def relay_scenario_add():
    relays = Relay.query.all()
    existingScenarioNames = [s.Name for s in RelayScenario.query.all()]
    app.logger.debug('Existing RelayScenario names: {}'.format(existingScenarioNames))

    class RelayScenarioAddForm(FlaskForm): pass
    setattr(RelayScenarioAddForm, 'name', StringField('Name', validators=[InputRequired(), Length(min=1, max=50), NoneOf(existingScenarioNames, message='Name already exist')]))
    for relay in relays:
        # app.logger.debug('RelayID={}'.format(relay.RelayID))
        setattr(RelayScenarioAddForm, 'RelayID={}'.format(relay.RelayID), RadioField('State for {} \'{}\''.format(relay.RelayID, relay.Name), choices=[('1', 'On'), ('0', 'Off'), ('-1', 'Not set')], default='-1', coerce=str, validators=[InputRequired()]))
    setattr(RelayScenarioAddForm, 'submit', SubmitField('Save'))

    form = RelayScenarioAddForm()
    if form.validate_on_submit():
        # Saving RelayScenario name
        scenario = RelayScenario(form.name.data)
        db.session.add(scenario)
        db.session.commit()
        relayScenarioID = scenario.RelayScenarioID

        # Saving setup for RelayScenario
        for field in form:
            if field.name.split('=')[0] == 'RelayID':
                relayID = field.name.split('=')[1]
                if field.data == '1':
                    relayState = True
                elif field.data == '0':
                    relayState = False
                else:
                    relayState = None

                app.logger.debug('RelayScenarioID: {}, RelayID: {}, RelayState: {}'.format(relayScenarioID, relayID, relayState))

                if relayState != None:
                    setup = RelayScenarioSetup(relayScenarioID, relayID, relayState)
                    db.session.add(setup)

        db.session.commit()

        flash('RelayScenario \'{}\' has been added!'.format(scenario.Name))

        return redirect(url_for('relay_scenario'))

    return render_template('relayscenario_manipulate.html', form=form)

@app.route('/relayscenario/modify/<int:scenarioID>', methods=['GET', 'POST'])
@login_required
def relay_scenario_modify(scenarioID):
    relays = Relay.query.all()
    existingScenarioNames = [s.Name for s in RelayScenario.query.all()]
    app.logger.debug('Existing RelayScenario names: {}'.format(existingScenarioNames))

    scenario = RelayScenario.query.get(scenarioID)

    relaysInScenario = list() # List containing relays used in scenario
    for i in scenario.Setup.all():
        relaysInScenario.append(i.RelayID)
    app.logger.debug('relaysInScenario: {}'.format(relaysInScenario))
    if scenario.Name in existingScenarioNames: # Deletes existing scenario name in order to validate_on_submit
        existingScenarioNames.remove(scenario.Name)

    class RelayScenarioEditForm(FlaskForm): pass
    setattr(RelayScenarioEditForm, 'name', StringField('Name', default=scenario.Name, validators=[InputRequired(), Length(min=1, max=50), NoneOf(existingScenarioNames, message='Name already exist')]))
    for relay in relays:
        if relay.RelayID in relaysInScenario:
            relayScenarioSetup = scenario.Setup.filter_by(RelayID=relay.RelayID).first()
            if relayScenarioSetup.State:
                relayDefault = '1'
            else:
                relayDefault = '0'
        else:
            relayDefault = '-1'

        setattr(RelayScenarioEditForm, 'RelayID={}'.format(relay.RelayID), RadioField('State for {} \'{}\''.format(relay.RelayID, relay.Name), choices=[('1', 'On'), ('0', 'Off'), ('-1', 'Not set')], default=relayDefault, coerce=str, validators=[InputRequired()]))
    setattr(RelayScenarioEditForm, 'submit', SubmitField('Save'))
    setattr(RelayScenarioEditForm, 'delete', SubmitField('Delete scenario'))

    form = RelayScenarioEditForm()
    if form.validate_on_submit():
        app.logger.debug('form.submit: {}, form.delete: {}'.format(form.submit.data, form.delete.data))
        if form.submit.data:
            # Saving RelayScenario name
            scenario.Name = form.name.data
            relayScenarioID = scenario.RelayScenarioID
            # Deleting exsisting RelayScenarioSetups
            RelayScenarioSetup.query.filter_by(RelayScenarioID=relayScenarioID).delete()

            # Saving setup for RelayScenario
            for field in form:
                if field.name.split('=')[0] == 'RelayID':
                    relayID = field.name.split('=')[1]
                    if field.data == '1':
                        relayState = True
                    elif field.data == '0':
                        relayState = False
                    else:
                        relayState = None

                    app.logger.debug('RelayScenarioID: {}, RelayID: {}, RelayState: {}'.format(relayScenarioID, relayID, relayState))

                    if relayState != None:
                        setup = RelayScenarioSetup(relayScenarioID, relayID, relayState)
                        db.session.add(setup)

            db.session.commit()

            flash('RelayScenario \'{}\' has been edited!'.format(scenario.Name))

            return redirect(url_for('relay_scenario'))
        elif form.delete.data:
            db.session.delete(scenario)
            db.session.commit()

            flash('RelayScenario \'{}\' has been deleted!'.format(scenario.Name))

            return redirect(url_for('relay_scenario'))
        else:
            app.logger.error('Unknown error occured!')

    return render_template('relayscenario_manipulate.html', form=form)

@app.route('/relayscenario/activate', methods=['POST'])
@login_required
def relay_scenario_activate():
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
