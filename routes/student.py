from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re
from lib.check_user import check_user

student_bp = Blueprint("student", __name__, url_prefix="/student")

#STUDENT ROUTES
@student_bp.route("/")
def student():
    return redirect(url_for("student.student_dashboard"))
    

@student_bp.route("/menu", methods = ['GET'])
def student_dashboard():
    user_check = check_user(session)
    if(user_check == "student"):
            classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"15"}, {"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023","profesor":"pedro gomez","cedula_profesor":"5535","nota":"05"},{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"2-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"20"}, {"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"3-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"12"}]
            return render_template("student/studentDashboard.html", classes=classes)
    else:
        return redirect(url_for("login.login"))    

@student_bp.route("/profile", methods = ['GET'])
def student_profile():
    user_check = check_user(session)
    if(user_check == "student"):
        return render_template("student/studentProfileEdit.html")

    else:
        return redirect(url_for("login.login"))  


    

