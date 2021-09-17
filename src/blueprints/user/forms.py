from flask_wtf import FlaskForm
from flask_wtf import file
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets.core import CheckboxInput
from flask_wtf.file import FileField, FileAllowed, FileRequired


from .models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "username", validators=[DataRequired(), Length(min=4, max=24)]
    )
    email = EmailField(
        "email", validators=[DataRequired(), Email(), Length(min=6, max=88)]
    )
    password = PasswordField(
        "password", validators=[DataRequired(), Length(min=4, max=32)]
    )
    confirm_password = PasswordField(
        "ConfirmPassword", validators=[DataRequired(), EqualTo("password")]
    )

    role = StringField("role", validators = [DataRequired()])

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )
        
        return True

    def validate_email_password(self, email, password):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email/password is taken. Please choose a different one.")
        
        user__ = User.query.filter_by(password = generate_password_hash(password.data, method='sha256')).first()

        if user__:
            raise ValidationError("That email/password is taken. Please choose a different one.")
        
        return True



class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[DataRequired(), Length(min=4, max=24)]
    )
    password = PasswordField("password", validators=[DataRequired()])
    
    remember = BooleanField('remember me')

    submit = SubmitField("Login")

class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('Crop')

class UploadAvatarForm(FlaskForm):
    file = FileField('Upload (<=3M)', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField()

class TeacherProfile(FlaskForm):
    price_per_hour = IntegerField(
        "price_per_hour",
    )
    thumbnaildescription = StringField("thumbnaildescription", validators = [DataRequired(), Length(max = 300)])
    description = StringField("description", validators = [DataRequired(), Length(max = 5000)])
    years = IntegerField("years",)
    language = StringField("language", validators = [DataRequired()])
    phone = IntegerField("phone", validators = [Optional()]) # only visible to admin


class StudentProfile(FlaskForm):
    name = StringField("name", validators = [DataRequired(), Length(max = 25)])
    language = StringField("language", validators = [DataRequired()])
    phone = IntegerField("phone", validators = [Optional()]) # only visible to admin
