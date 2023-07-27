from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re

root_bp = Blueprint("root", __name__)

@root_bp.route('/')
def root():
    return redirect(url_for("login.login"))