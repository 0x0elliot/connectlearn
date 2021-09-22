import time
from datetime import datetime
from flask import Blueprint, render_template, request, current_app, abort, redirect
from flask_login import current_user, login_required
from flask_mail import Message
from wtforms.validators import Email
from .forms import contact_form
from ..user.models import User, EmailsMade
from threading import Thread

import os
import sys

from src.extension import mail,db

contact = Blueprint("contact", __name__, url_prefix = "/contact", template_folder = "../../templates/contact/")


class FlaskThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()

def send_email(title, message_to_send, sender, email, emailbyuserid, emailtouserid,):
    msg = Message(subject = title, body = message_to_send, sender = sender)
    msg.recipients = [email] 
    mail.send(msg)

    emailmade = EmailsMade(emailbyuserid = emailbyuserid,
        emailtouserid = emailtouserid,
        unixtime = str(int(time.time())),
        message = message_to_send)
    
    db.session.add(emailmade)
    db.session.commit()

#add last two functions in utils.py

#rate limit endpoint by saving in a db the number of requests made by account and then limit accordingly
@contact.route('/<id>', methods = ["GET", "POST"])
@login_required
def reach_out(id):

    user = User.query.filter_by(id = id).first()

    if user == None:
        abort(404)

    form = contact_form()

    if form.validate_on_submit():
        emailsmade = EmailsMade.query.filter_by(emailbyuserid = current_user.id)
        if emailsmade.first():
            for i in emailsmade: # continue here
                unixtime_then = int(i.unixtime) #unix time stamp of the time the email was sent
                unixtime_now =  int(time.time()) #unix time stamp of now

                time_difference = int((unixtime_now - unixtime_then)/(60*60*24)) #number of days that has passed since last contact
                if time_difference == 0:
                    return render_template("contact.html", form = form, message_from_server = "You have already tried reaching this person today. Try again tomorrow.")
        

        title_suffix = " scheduled a class with you!"
        title = current_user.username + title_suffix #make sure to limit the username to 20 characters
        name = current_user.name

        if current_user.name == None:
            name = current_user.username

        phone_line = ""
        if form.usephone.data:
            phone_line = f"Their Phone Number is: {current_user.phone}"

        message_to_send = f"""
{name} wants to schedule a class with you. 
Their email is: {current_user.email}.
Their Name is: { "[Not Clarified!]" if current_user.name == None else current_user.name}""" + "\n" + phone_line +f"""
Their message is:
{form.message.data} 
"""

        FlaskThread(target = send_email, args = (title, message_to_send, os.environ.get("MAIL_USERNAME"), user.email, current_user.id, id)).start() #make this more organised and better at preventing spam
        return render_template("contact.html", message_from_server = "Message sent. You will be contacted by the teacher now.", form = form) 

    return render_template("contact.html", form = form)