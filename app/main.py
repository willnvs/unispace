# main.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import login_required, current_user
import re
import secrets

main = Blueprint('main', __name__)

# define Database
db = SQLAlchemy()

  
#### LOGIC TO CREATE / SHOW THE DASHBOARD ####

@main.route('/dashboard')
@login_required
def profile():
    email = current_user.email
    password = current_user.password
    from .models import Messages
    email = current_user.email
    # return all lists for the current user except shared lists 
    query = "SELECT photo, name from user order by name asc".format() 
    rows = db.session.execute(query)
    output = rows.fetchall()
    messages = Messages.query.order_by(Messages.date_created).filter_by(course_name='DCU - GDWT').all()
 

    return render_template('profile.html', name=current_user.name, photo=current_user.photo, tasks=messages, email=email, password=password, output=output)

    
 