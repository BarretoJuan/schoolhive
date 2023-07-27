from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re

student_bp = Blueprint("student", __name__, url_prefix="/student")

#STUDENT ROUTES
@student_bp.route("/")
def student():
    return redirect(url_for("student.student_dashboard"))

@student_bp.route("/menu")
def student_dashboard():
    classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"15"}, {"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023","profesor":"pedro gomez","cedula_profesor":"5535","nota":"05"},{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"2-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"20"}, {"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"3-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"12"}]
    return render_template("student/studentDashboard.html", classes=classes)

@student_bp.route("/profile")
def student_profile():
    return render_template("student/studentProfileEdit.html")

#TEST ROUTE
@student_bp.route("/test")
def test():
    return render_template("/admin/adminMajor/majorMenu.html")

