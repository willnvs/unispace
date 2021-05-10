# init.py

from flask import Blueprint, Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os 
import secrets # only works with python 3.6 or above
from os.path import join, dirname, realpath


# define Database
db = SQLAlchemy()

# function to create the application / set configuration

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['UPLOAD_FOLDER'] = 'static/upload/profile/'
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 2 # LIMIT SIZE FOR UPLOADS FILES - 2 MB
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # SET SUPPORTED FILES
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    db.init_app(app)


    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    #### LOGIC TO SEND MESSAGES  ####
    
    @app.route('/insert', methods=['POST', 'GET'])
    def insert():        
        
        from .models import Messages
        email = current_user.email
        name = current_user.name
        photo = current_user.photo

        course_name = 'DCU - GDWT'

        #getting information from the form to send the message
        if request.method == 'POST':
            message_content = request.form['content'] # this will receive the input data from the form using the id of the input  
 
        #passing values to the system in order to add the message
            new_message = Messages(content=message_content, email=email, course_name=course_name, name=name, photo=photo)

            
            try: 
                db.session.add(new_message)
                db.session.commit()
   

                return redirect(request.referrer)


            except: 
                return 'There was a problem sending this message.'

        else: 
            return redirect('/')



    #### LOGIC TO REMOVE MESSAGES ####

    @app.route('/remove/<int:id>')
    def delete(id):
        from .models import Messages    
        message_to_delete = Messages.query.get_or_404(id)
  

        try:
            db.session.delete(message_to_delete)
            db.session.commit()

 
            return redirect(request.referrer)

        except:
            return 'There was a problem deleting that message'



      #### LOGIC TO UPLOAD FILES ####


    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':    
            email = current_user.email
            #Get file1 object as file1

            file1 = request.files['fileF']
            random_hex = secrets.token_hex(20)
            _, f_ext = os.path.splitext(file1.filename)
            picture_fn = random_hex + f_ext
            basedir = os.path.abspath(os.path.dirname(__file__))
            picture_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], picture_fn)
            file1.save(picture_path)
              
 
 
            upload_photo = User.query.filter_by(email=current_user.email).update(dict(photo=picture_fn))
            db.session.commit()
            db.session.flush()
            from .models import Messages    
            upload_photo_messages = Messages.query.filter_by(email=current_user.email).update(dict(photo=picture_fn))
            db.session.commit()
            db.session.flush()
            return redirect(request.referrer)


     
    
    if __name__ == "__main__": 
        app.run(debug=True)

    return app


 
 