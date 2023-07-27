from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re

professor_bp = Blueprint("professor", __name__, url_prefix="/professor")

#PROFESSOR ROUTES
@professor_bp.route("/")
def professor():
    return redirect(url_for("professor.professor_dashboard"))

@professor_bp.route("/menu")
def professor_dashboard():
    classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
              {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("professor/professorDashboard.html", classes=classes, sections=sections, terms=terms)

@professor_bp.route("/profile")
def professor_profile():
    return render_template("professor/professorProfileEdit.html")

@professor_bp.route("/class-") #implement id
def professor_class():
    students=[{"name":"roberto roberto", "cedula":"555","nota":"20"},{"name":"pedro roberto", "cedula":"455","nota":"10"},{"name":"ramon roberto", "cedula":"44","nota":"14"},{"name":"enrique roberto", "cedula":"33","nota":"05"}]
    return render_template("professor/professorClass.html", students=students)


