from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from base.models import User
from flask_login import login_user, current_user


class Registration(FlaskForm):
    username = StringField('Username',validators=[ DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')]) 
    submit= SubmitField('SignUp')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Validation Error: Username is taken already.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Validation Error: email is taken already.')
    
    
class Login(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit= SubmitField('Login')
    
    
class UpdateAcountForm(FlaskForm):
    username = StringField('Username',validators=[ DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit= SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username: 
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Validation Error: Username is taken already.')
    
    def validate_email(self, email):
        if email.data != current_user.email: 
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Validation Error: email is taken already.')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit= SubmitField('Request Password Reset')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')]) 
    submit= SubmitField('Reset Password')    