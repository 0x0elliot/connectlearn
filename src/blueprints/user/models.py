from src.extension import login_manager, db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(255),
    unique = True,
    index = True,
    nullable = False
    ) #email would be visible to all

    role = db.Column(db.String, nullable = False,index = True) #student/teacher/admin
    username = db.Column(db.String(24), unique = True, index = True)
    password = db.Column(db.String(128), unique = True, nullable = False)
    name = db.Column(db.String(128), nullable = True) #only for students
    active = db.Column('is_active', db.Boolean(), nullable = False, server_default = '1') #To satisfy flask_login. Activating and deactivating user. 1 represents true.


    #teacher only stuff
    price_per_hour = db.Column(db.Integer, nullable = True, server_default = "15") #in dollars. nullable because just in case they want this to be negotiable
    thumbnaildescription = db.Column(db.String, nullable = True, server_default = "Hey! I teach really well!")
    description = db.Column(db.String, nullable = True, server_default = "Contact me by pressing the button!")
    years = db.Column(db.Integer, server_default = "0",) # Years of experience. Might need to change this up later. 0 stands for less than 1 year.
    language = db.Column(db.String, server_default = "english", index = True) # select multiple
    profile_setup_status = db.Column(db.Boolean(), server_default = '0', index = True) #if they have initiated their profile. 1 stands for false.
    phone = db.Column(db.String) #Saving it as a strive so that I can save it in +(country code) (phone number) format. Also visible to all.
    profile_picture_url = db.Column(db.String, server_default = None, index = True) #temp file name for cropping. use avatars
    account_made_on = db.Column(db.String)

    avatar = db.Column(db.String(64), server_default = None) #use this for avatar stuff.
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

class EmailsMade(db.Model):
    __tablename__ = "emailsmade"
    id = db.Column(db.Integer, primary_key = True)
    emailbyuserid = db.Column(db.Integer)
    emailtouserid = db.Column(db.Integer)
    unixtime = db.Column(db.String)
    message = db.Column(db.String)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))