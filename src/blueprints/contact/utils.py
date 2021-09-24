import time
from threading import Thread
from flask import current_app
from flask_mail import Message
from src.extension import mail,db
from datetime import datetime
from ..user.models import User, EmailsMade

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