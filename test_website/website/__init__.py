from flask import Flask
from os import path
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO


db = SQLAlchemy()
DB_NAME = "users.db"

def importing():
    from website.auth import login

importing()

def create_app():

    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'ga8925asdgDgls10352;aDg'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    ma = Marshmallow(app)

    from .views import views
    from .auth import auth
    from .rooms import rooms
    from .profiles import profiles

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(rooms, url_prefix='/rooms/')
    app.register_blueprint(profiles, url_prefix='/user/')

    from .models import User, Empires, Game, GamesJoined
    
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

        