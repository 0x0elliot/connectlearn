import time
from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, session, escape, abort
from flask_wtf import form
from flask_login import login_user, current_user, login_required, logout_user
from wtforms.validators import Email, ValidationError
from .forms import RegistrationForm, LoginForm, TeacherProfile, StudentProfile,UploadAvatarForm
from werkzeug.security import generate_password_hash, check_password_hash
from  werkzeug.utils import secure_filename
from .models import User

import os
import sys
import subprocess
avatars_in_directory = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../avatars/"))

from src.extension import db, login_manager, avatars, _avatars

user = Blueprint('user', __name__, template_folder = "../../templates/user/", url_prefix = "/user")

@login_manager.unauthorized_handler 
def unauthorized_callback():
    print("unauthenticated")
    return redirect("/user/login") 

@user.route('/login', methods = ["GET", "POST"])
def user_login():
    form = LoginForm(meta={'csrf': False})

    if form.validate_on_submit():
        user_obj = User.query.filter_by(username=form.username.data).first()
        if user_obj:
            if check_password_hash(user_obj.password, form.password.data):
                print("authenticating")
                login_user(user_obj, remember=form.remember.data)

                if user_obj.role == "teacher":
                    if user_obj.profile_setup_status == False:
                        return redirect('/user/profile/edit')

                    return redirect('/')
                    
                elif user_obj.role == "student":
                    if user_obj.profile_setup_status == False:
                        return redirect('/user/profile/edit')
                    return redirect('/')
            else:
                return render_template('login_register/login.html', message = "Invalid Username/Password", form = form)
        
        else:
            return render_template('login_register/login.html', message = "Invalid Username/Password", form = form)

    return render_template('login_register/login.html', message = "Fill the form to login", form = form)

@user.route('/register', methods = ["GET", "POST"])
def user_register():

    form = RegistrationForm(meta={'csrf': False})

    if form.validate_on_submit():
        if form.role.data in ["student", "teacher"]:
            try:
                if (form.validate_email_password(form.email, form.password) and form.validate_username(form.username)):
                    hashed_password = generate_password_hash(form.password.data, method='sha256') #shift to bcrypt
                    if current_user.is_authenticated:
                        logout_user()

                    new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, role = form.role.data, name = form.username.data, account_made_on = int(time.time()))
                    db.session.add(new_user)
                    db.session.commit()
                    return render_template("login_register/register.html", form = form, message = "User successfully registered!")
                
                return render_template("login_register/register.html", form = form, message = "This condition shouldn't be possible. Contact the devs.") # comment out after testing

            except ValidationError as e:
                print(e, form.errors)
                return render_template('login_register/register.html', form = form, message = str(e))
        
        return render_template("login_register/register.html", message = form.errors, form = form)

    return render_template("login_register/register.html", form = form, message = form.errors)


@user.route('/logout')
@login_required
def logout_():
    logout_user()

    return redirect("/user/login")




@user.route('/profile/edit', methods = ["GET", "POST"])
@login_required
def setup_profile():
    english_selected = ""
    korean_selected = ""
    japanese_selected = ""
    mandarin_selected = ""
    cantonese_selected = ""
    if current_user.role == "student":
        form = StudentProfile()
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.phone = form.phone.data

            if form.language.data in ["english", "korean", "japanese", "mandarin", "cantonese"]:
                current_user.language = form.language.data

            current_user.profile_setup_status = True
            
            db.session.commit()

            if current_user.language == "english":
                english_selected = "english selected"
        
            elif current_user.language == "korean":
                korean_selected = "korean selected"
        
            elif current_user.language == "japanese":
                japanese_selected = "japanese selected"
        
            elif current_user.language == "mandarin":
                mandarin_selected = "mandarin selected"
        
            elif current_user.language == "cantonese":
                cantonese_selected = "cantonese selected"
            
            

            return render_template("profile/studenteditprofile.html", form = form, username = current_user.username, email = current_user.email, phone = current_user.phone, name = current_user.name, language = current_user.language,
            english_selected = english_selected,
            korean_selected = korean_selected,
            japanese_selected = japanese_selected,
            mandarin_selected = mandarin_selected,
            cantonese_selected = cantonese_selected,)
        
        return render_template('profile/studenteditprofile.html', form = form,  name = current_user.name, language = current_user.language, username = current_user.username, email = current_user.email, phone = current_user.phone,
            english_selected = english_selected,
            korean_selected = korean_selected,
            japanese_selected = japanese_selected,
            mandarin_selected = mandarin_selected,
            cantonese_selected = cantonese_selected)


    form = TeacherProfile()
    print(request.method)
    if current_user.role == "teacher":

        if form.validate_on_submit():


            current_user.price_per_hour = form.price_per_hour.data 
            current_user.thumbnaildescription = form.thumbnaildescription.data
            current_user.description = form.description.data

            if form.years.data >= 0:
                current_user.years = form.years.data

            if form.language.data in ["english", "korean", "japanese", "mandarin", "cantonese"]:
                current_user.language = form.language.data

            current_user.phone = form.phone.data

            if current_user.profile_setup_status == False:
                current_user.profile_setup_status = True

            db.session.commit() # save user info submitted

        price_per_hour = current_user.price_per_hour 
        
        if current_user.phone == None:
            phone = None
        
        elif current_user.phone != None:
            phone = current_user.phone
        
        thumbnaildescription = current_user.thumbnaildescription 
        description = current_user.description

        print(current_user.language)
        if current_user.language == "english":
            english_selected = "english selected"
        
        elif current_user.language == "korean":
            korean_selected = "korean selected"
        
        elif current_user.language == "japanese":
            japanese_selected = "japanese selected"
        
        elif current_user.language == "mandarin":
            mandarin_selected = "mandarin selected"
        
        elif current_user.language == "cantonese":
            cantonese_selected = "cantonese selected"

        years = current_user.years     

        return render_template('/profile/teachereditprofile.html',
        price_per_hour = price_per_hour,
        phone = phone,
        thumbnaildescription = thumbnaildescription,
        description = description,
        english_selected = english_selected,
        korean_selected = korean_selected,
        japanese_selected = japanese_selected,
        mandarin_selected = mandarin_selected,
        cantonese_selected = cantonese_selected,

        form = form, 
        username = current_user.username, 
        email = current_user.email, 
        current_user = current_user, 
        avatars = avatars,
        years = years,
        )

    return redirect('/')


@user.route('/avatars/<path:filename>')
def get_avatar(filename):
    if filename[-4:] in [".png", ".jpg"] or filename[-5:] == ".jpeg":
        return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], secure_filename(filename))
    
    return "Something went wrong. This would be logged and investigated."

@user.route('/setup/upload', methods = ["GET", "POST"])
@login_required
def teacher_profile_upload(): #add code to delete previous pictures user uploaded from the server to keep the server clean
    form = UploadAvatarForm()
    if current_user.role == "teacher":
        if (form.validate_on_submit() and request.method == "POST"):
            f = request.files.get('file')
            raw_filename = avatars.save_avatar(f)
            current_user.profile_picture_url = raw_filename #to be used later in /user/setup/crop
            db.session.commit()

            return redirect('/user/setup/crop')

        return render_template("/profile/imageupload.html", form = form, avatars = avatars)

    return redirect('/user/profile',) #

@user.route('/setup/crop', methods = ["GET", "POST"])
@login_required
def teacher_pfp_crop():
    if current_user.role == "teacher":
        if request.method == "POST":
            x = request.form.get('x')
            y = request.form.get('y')
            w = request.form.get('w')
            h = request.form.get('h')
            filenames = avatars.crop_avatar(current_user.profile_picture_url, x, y, w, h)
            print(filenames)
            current_user.avatar = filenames[2]
            print(filenames[1])

            db.session.commit()
            all_existing_users = User.query.all() #change this bit of code when the site becomes too big.
            all_user_pfp_paths = [i.avatar for i in all_existing_users]
        
            avatars_in_directory = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../avatars/"))

            for avtr in avatars_in_directory:
                if avtr not in all_user_pfp_paths:
                    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../avatars/", avtr)) # should clean everything up

            #return render_template('/profile/done_crop.html', avatars = avatars)
            return redirect("/user/profile/edit")
            
        image_url_local = current_app.config['AVATARS_SAVE_PATH'] + current_user.profile_picture_url
        #return redirect("/profile/"+str(current_user.id))
    
    return render_template('profile/crop.html')


@user.route('/profile/<id>') #profile feature is only for teachers at the moment.
@login_required
def view_profile(id):

    user = User.query.filter_by(id = id).first()

    if user:
        return render_template('/profile/profile.html', user = user)
    
    abort(404) # if no user found, give a 404
