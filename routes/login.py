from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re

login_bp = Blueprint("login", __name__, url_prefix="/login")

#LOGIN ROUTES
@login_bp.route("/")
def login():
    return render_template("/auth/loginOptions.html")

@login_bp.route("/admin")
def login_admin():
    return render_template("/auth/loginAdmin.html")

@login_bp.route("/student")
def login_student():
    return render_template("/auth/loginStudent.html")

@login_bp.route("/professor")
def login_professor():
    return render_template("/auth/loginProfessor.html")

