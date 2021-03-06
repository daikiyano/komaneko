import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_script import Manager
from flask_mail import Mail
from config import Config





app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
######################################
###############databwse############
########################

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
db = SQLAlchemy(app)
Migrate(app,db,compare_type=True)
manager.add_command('db', MigrateCommand)
mail = Mail(app)



if __name__ == '__main__':
    manager.run()


##########################
#####login configs

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'




from companyblog.core.views import core
from companyblog.users.views import users
from companyblog.blog_posts.views import blog_posts
from companyblog.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)
