from flask import Blueprint, render_template, request, current_app, abort, redirect
from flask_login import login_required
from sqlalchemy import desc, asc
from ..user.models import User

from datetime import datetime
import os
import sys

from src.extension import mail,db

main = Blueprint("main", __name__, template_folder = "../../templates/main/")

@main.route('/') #divide this into 25 results per page.
@login_required
def home():
    search = False

    username = request.args.get("username")
    time = request.args.get("time")
    language = request.args.get("language")
    priceperhour = request.args.get("priceperhour")

    last_key = 0

    data = {}
    

    # below is code if searching is used
    if username != None: #does the job better
        if time == None or time == "":
            users = User.query.filter_by(role = "teacher").all()
        elif time == "Most Recent":
            users = User.query.filter_by(role = "teacher").order_by(desc(User.account_made_on)).all()
        elif time == "Most Oldest":
            users = User.query.filter_by(role = "teacher").order_by(asc(User.account_made_on)).all()

        if language != None and language != "" and language in ["english", "korean", "japanese", "mandarin", "cantonese"]:
            to_remove = []
            for i in users:
                if i.language != language:
                    to_remove.append(i)

            for j in to_remove:
                users.remove(j)
        
        if priceperhour != None and priceperhour in ["15$-25$", "25$-35$", "35$-50$", "above 50$"]:
            to_remove = []

            if priceperhour == "15$-25$":
                lower_limit = 15
                upper_limit = 25
            elif priceperhour == "25$-35$":
                lower_limit = 25
                upper_limit = 35
            elif priceperhour == "35$-50$":
                lower_limit = 35
                upper_limit = 50
            elif priceperhour == "above 50$":
                lower_limit = 50
                upper_limit = 1000

            for i in users:
                print(lower_limit, upper_limit,i.price_per_hour)
                if (lower_limit <= i.price_per_hour <= upper_limit) == False:   
                    to_remove.append(i)

            for j in to_remove:
                users.remove(j)

        search = True 
        for i in users:
            if username in i.username:
                user_obj = i

                if len(data) != 0:
                    last_key = list(data.keys())[-1]

                data[last_key+1] = {"id" : user_obj.id,
                "username" : user_obj.username,
                "language" : user_obj.language,
                "priceperhour" : user_obj.price_per_hour,
                "thumbnaildescription" : user_obj.thumbnaildescription,
                "avatar" : user_obj.avatar,
                "date" : int(user_obj.account_made_on),
                "experience": "Less Than 1 Year" if user_obj.years == 0 else str(user_obj.years) + " Years"
                }
            
            elif username.lower() in i.thumbnaildescription.lower() or username.lower() in i.description.lower():
                user_obj = i

                if len(data) != 0:
                    last_key = list(data.keys())[-1]

                data[last_key+1] = {"id" : user_obj.id,
                "username" : user_obj.username,
                "language" : user_obj.language,
                "priceperhour" : user_obj.price_per_hour,
                "thumbnaildescription" : user_obj.thumbnaildescription,
                "avatar" : user_obj.avatar,
                "date" : int(user_obj.account_made_on),
                "experience": "Less Than 1 Year" if user_obj.years == 0 else str(user_obj.years) + " Years"
                }
        
    #if home page is called with no searching

    elif search == False:
        users = User.query.filter_by(role = "teacher").all()
        for i in users:
            user_obj = i
            last_key = 0

            if len(data) != 0:
                last_key = list(data.keys())[-1]

            data[last_key+1] = {"id" : user_obj.id,
            "username" : user_obj.username,
            "language" : user_obj.language.capitalize(),
            "priceperhour" : user_obj.price_per_hour,
            "thumbnaildescription" : user_obj.thumbnaildescription,
            "avatar" : user_obj.avatar,
            "date" : int(user_obj.account_made_on),
            "experience": "Less Than 1 Year" if user_obj.years == 0 else str(user_obj.years) + " Years"
            }

    return render_template('home.html', data = data, search = search)