from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, PasswordField, SubmitField, validators, IntegerField, TextAreaField, FileField, BooleanField
from wtforms.validators import InputRequired, ValidationError
import re
from app.custom_regex import email as reg_email

## Custom Validators ##

def validate_email(FlaskForm, field):
    if not (re.search(reg_email, field.data)) or (len(field.data) > 300):
        raise ValidationError('Please enter a valid email')

def validate_length(name, value):
    def _length(FlaskForm, field):
        if len(field.data) < value:
            raise ValidationError(f'{name} must be a minimum {value} characters')
    return _length

def validate_passwords(FlaskForm, field):
    if field.data != request.form.get('password'):
        raise ValidationError('Both password must match')

def validate_image(FlaskForm, field):
    supported_files = ('.png', '.jpg', '.jpeg', 'gif')
    if not str(field.data.filename).endswith(supported_files):
        raise ValidationError('Image type is not supported. Please upload one of the following: .png, .jpg, .jpeg or .gif')


## Auth Forms ##

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), validate_email])
    username = StringField(validators=[InputRequired(), validate_length('Username', 4)])
    password = PasswordField(validators=[InputRequired(), validate_length('Password', 8)])
    confirm_password = PasswordField(validators=[InputRequired(), validate_passwords])

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])

## List Forms

class CreateListForm(FlaskForm):
    list_name = StringField('List Name', validators=[InputRequired()])
    list_items = TextAreaField('List Items', validators=[InputRequired()])
    exploreable = BooleanField('Exploreable')

class EditListName(FlaskForm):
    list_name = StringField('List Name', validators=[InputRequired()])

class AddAdditionalListItems(FlaskForm):
    list_item = StringField('List Item', validators=[InputRequired()])

class AddManyListItems(FlaskForm):
    list_items = TextAreaField('List Items', validators=[InputRequired()])