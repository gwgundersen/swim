"""Configure and start the web server."""

from flask import Flask, g, session as flask_session
from flask.ext.login import LoginManager, current_user
from flask.ext.sqlalchemy import SQLAlchemy

from swim.config import config


""" Database configuration and app initialization
    -----------------------------------------------------------------------"""
# Create db first. Models all import this.
db = SQLAlchemy()

# Import models. They must be interpreted before creating the database.
from swim import models

app = Flask(__name__,
            static_url_path="%s/static" % config.get("url", "base"),
            static_folder="static")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s:3306/%s" % (
    config.get("db", "user"),
    config.get("db", "passwd"),
    config.get("db", "host"),
    config.get("db", "db")
)
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800  # Recycle every 30 min.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()


""" URL configuration
    -----------------------------------------------------------------------"""
app.config.base_tag_url = "/swim/"


""" Debugging
    -----------------------------------------------------------------------"""
# It's impossible to debug a 500 error in production without seeing an error
# message.
app.config["DEBUG"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True


""" Server endpoints
    -----------------------------------------------------------------------"""
from swim import endpoints
app.register_blueprint(endpoints.auth_blueprint)
app.register_blueprint(endpoints.index_blueprint)
app.register_blueprint(endpoints.task_blueprint)


""" Login session management
    -----------------------------------------------------------------------"""
# Change this key to force all users to re-authenticate.
app.secret_key = config.get("cookies", "secret_key")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@app.before_request
def before_request():
    """Set current user, if available, to be globally available."""
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(models.User).get(user_id)
    return user


@app.before_request
def make_session_permanent():
    """Sets Flask session to "permanent", meaning 31 days."""
    flask_session.permanent = True