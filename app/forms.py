from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, InputRequired, NumberRange

class LoginForm(FlaskForm):
    """Form class for user login."""
    # email = TextField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# class RelayScenarioAddForm(FlaskForm):
#     """Form class for adding new RelayScenarios."""
#     name = StringField('Name', validators=[InputRequired(), NumberRange(min=1, max=50)])
#
#     submit = SubmitField('Save')
