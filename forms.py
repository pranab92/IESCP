
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,EmailField,IntegerField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=15, message="Username must be between 2 and 15 characters.")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('*Username', validators=[DataRequired(),Length(min=2, max=15, message="Username must be between 2 and 15 characters.")])
    email = EmailField('*Email', validators=[DataRequired()])
    password = PasswordField('*Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class CampaignForm(FlaskForm):
    name = StringField('*Name', validators=[DataRequired(),Length(min=1, max=20, message="Name of Campaign must be between 1 and 20 chars.")])
    description = TextAreaField('Description')
    start_date = DateField('*Start Date', validators=[DataRequired()])
    end_date = DateField('*End Date', validators=[DataRequired()]) 
    budget = IntegerField('Budget')
    visibility = SelectField('Visibility', choices=[('Public'), ('Private')],validators=[DataRequired()])

    status = SelectField('Status', choices=[('Active'), ('Inactive')],validators=[DataRequired()])

    submit = SubmitField('Create Campaign')    
    save = SubmitField('Save')