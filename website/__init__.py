from flask import Flask, render_template
from os import path
from flask.app import _make_timedelta
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
import schedule
#these are the different imports used to create the database, create the web server,
#and handle certain things with logging in and out.


db = SQLAlchemy()
DB_NAME = "users.db"

def importing():
    from website.auth import login
importing()
#these statements all initialize various things, and the import statement there is in 
#a function to stop circular importing

def create_app():

    app = Flask(__name__)
    UPLOAD_FOLDER = 'static/pfp/'
    
    app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'ga8925asdgDgls10352;aDg'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOADS_DEFAULT_DEST'] = '/static/pfp/'
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    db.init_app(app)
    ma = Marshmallow(app)

    from .views import views
    from .auth import auth
    from .rooms import rooms
    from .profiles import profiles
    from .docs import docs

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(rooms, url_prefix='/rooms/')
    app.register_blueprint(profiles, url_prefix='/user/')
    app.register_blueprint(docs, url_prefix='/docs/')
    #these register the different paths, (they are in the different files) and sets the 
    #base path for them

    from .models import User
    
    create_database(app)
   

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
        
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database.')

