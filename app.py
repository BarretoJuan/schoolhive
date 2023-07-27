from flask import Flask
from flask_mysqldb import MySQL

from routes.login import login_bp
from routes.student import student_bp
from routes.admin import admin_bp
from routes.professor import professor_bp
from routes.root import root_bp
# Config:
from config import Config
# from lib.queue_message import messages

# Factory dispatches an instance of the app
def make_app():
    app = Flask(__name__)
    config = Config() # Build an instance of
    config.MYSQL = MySQL(app)
    app.config.from_object(config)

    app.register_blueprint(login_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(root_bp)
    return app


if __name__ == '__main__':
    app = make_app()
    app.run()





