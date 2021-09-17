from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class contact_form(FlaskForm):
    usephone = StringField("Phone Permission")
    message = StringField("Message", validators = [DataRequired(), Length(max = 500) ])