from flask import Flask, Blueprint
from flask_login import LoginManager

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config.from_envvar('APP_SETTINGS')

from .routes import main, auth
 
app.register_blueprint(main.main_bp) 
app.register_blueprint(auth.auth_bp)

from app.database import setup_db

setup_db(app, app.config['DATABASE_PATH'])

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)