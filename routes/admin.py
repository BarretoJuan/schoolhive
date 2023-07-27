from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

#ADMIN ROUTES
@admin_bp.route("/")
def admin():
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/menu")
def admin_dashboard():
    return render_template("admin/adminDashboard.html")

@admin_bp.route("/profile")
def admin_profile():
    return render_template("admin/adminProfileEdit.html")

#ADMIN/CLASS ROUTES
@admin_bp.route("/class-menu")
def admin_class_menu():
    classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
              {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
    print("classes? ",classes)
    return render_template("admin/adminClass/classMenu.html", classes=classes)

# @admin_bp.route("/admin/class-create")
# def admin_class_create():
#     return render_template("admin/adminClass/classCreate.html")

@admin_bp.route("/class-assign") #implement major by id
def admin_class_assign():
    classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
              {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("admin/adminClass/classAssign.html",classes=classes, sections=sections, terms=terms)

@admin_bp.route("/class-") #implement major by id
def admin_class():
    classs = {"nombre":"Calculo IV", "periodo":"1-2023","seccion":"n-613","profesor":"jose jose"}
    students = [{"nombre":"student1", "cedula":"5566"},{"nombre":"student2", "cedula":"55466"}]
    return render_template("admin/adminClass/class.html", classs=classs, students=students)

#ADMIN/MAJOR ROUTES
@admin_bp.route("/major-menu")
def admin_major_menu():
    majors=[{"major_name": "Ingenieria informática"}, {"major_name":"ingeniería electrónica"}]
    print("majors? ",majors)
    return render_template("admin/adminMajor/majorMenu.html", majors=majors)

@admin_bp.route("/major-create")
def admin_major_create():
    return render_template("admin/adminMajor/majorCreate.html")

@admin_bp.route("/major-edit") #implement major by id
def admin_major_edit():
    return render_template("admin/adminMajor/majorEdit.html")

@admin_bp.route("/major-") #implement major by id
def admin_major():
    major={"nombre":"Ingenieria informática"}
    students=[{"nombre":"roberto roberto", "cedula":"555"},{"nombre":"pedro roberto", "cedula":"455"},{"nombre":"ramon roberto", "cedula":"44"},{"nombre":"enrique roberto", "cedula":"33"}]
    classes=[{"nombre":"calculo IV", "periodo":"1-2023", "seccion":"n-613", "profesor":"roberto jose", "cedula_profesor":"5533", "num_participantes":"30"}, {"nombre":"calculo IV", "periodo":"1-2023", "seccion":"n-613", "profesor":"roberto jose", "cedula_profesor":"5533", "num_participantes":"30"}]

    return render_template("admin/adminMajor/major.html", major=major,students=students,classes=classes)

#ADMIN/PROFESSOR ROUTES
@admin_bp.route("/professor-menu")
def admin_professor_menu():
    professors=[{"professor_name": "Ramón Ramírez", "professor_cedula": "10444777"}, {"professor_name":"Jose Jose Sr.", "professor_cedula": "10555777"}]
    print("professors? ",professors)
    return render_template("admin/adminProfessor/professorMenu.html", professors=professors)

@admin_bp.route("/professor-create")
def admin_professor_create():
    return render_template("admin/adminProfessor/professorCreate.html")

@admin_bp.route("/professor-enroll") #implement professor by id
def admin_professor_enroll():
    classes=[{"class_name":"Cálculo IV"},{"class_name":"Geometría"},{"class_name":"Cálculo III"},{"class_name":"Programación III" }]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("admin/adminProfessor/professorEnroll.html", classes=classes, sections=sections, terms=terms)

@admin_bp.route("/professor-") #implement professor by id
def admin_professor():
    classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023"}, {"nombre_materia":"calculo III", "seccion":"n613", "periodo":"1-2023"}]
    professor = {"nombre":"José José", "cedula":"5478487"}
    return render_template("admin/adminProfessor/professor.html", classes=classes, professor=professor)

#ADMIN/SECTION ROUTES
@admin_bp.route("/section-menu")
def admin_section_menu():
    sections=[{"section_name": "N-613"}, {"section_name":"C-613"}]
    print("sections? ",sections)
    return render_template("admin/adminSection/sectionMenu.html", sections=sections)

@admin_bp.route("/section-create")
def admin_section_create():
    majors = [{"major_name":"ingenieria informatica"},{"major_name":"ingenieria electronica"},{"major_name":"contaduria"}]
    return render_template("admin/adminSection/sectionCreate.html", majors = majors)

@admin_bp.route("/section-") #implement section by id
def admin_section():
    classes  = [{"nombre_materia":"calculo IV", "periodo":"1-2023", "profesor":"roberto jose", "num_participantes":"30"}, {"nombre_materia":"calculo IV", "periodo":"1-2023", "profesor":"roberto jose", "num_participantes":"10"}]
    section = {"nombre":"C613", "carrera":"Ingeniería en computación"}
    return render_template("admin/adminSection/section.html", classes=classes, section=section)

#ADMIN/STUDENT ROUTES
@admin_bp.route("/student-menu")
def admin_student_menu():
    students=[{"student_name": "Ramón Rodríguez", "student_cedula": "31444777"}, {"student_name":"José José", "student_cedula": "31555777"}]
    
    print("students? ",students)
    return render_template("admin/adminStudent/studentMenu.html", students=students)

@admin_bp.route("/student-create")
def admin_student_create():
    return render_template("admin/adminStudent/studentCreate.html")

@admin_bp.route("/student-enroll") #implement student by id
def admin_student_enroll():
    classes=[{"class_name":"Cálculo IV"},{"class_name":"Geometría"},{"class_name":"Cálculo III"},{"class_name":"Programación III" }]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("admin/adminStudent/studentEnroll.html", classes=classes, sections=sections, terms=terms)

@admin_bp.route("/student-") #implement student by id
def admin_student():
    classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023"}, {"nombre_materia":"calculo III", "seccion":"n613", "periodo":"1-2023"}]
    student = {"nombre":"José José", "cedula":"5478487"}
    return render_template("admin/adminStudent/student.html", classes=classes, student=student)

#ADMIN/TERM ROUTES
@admin_bp.route("/term-menu")
def admin_term_menu():
    terms=[{"term_name": "1-2023"}, {"term_name":"2-2023"}]
    print("terms? ",terms)
    return render_template("admin/adminTerm/termMenu.html", terms=terms)

@admin_bp.route("/term-create")
def admin_term_create():
    return render_template("admin/adminTerm/termCreate.html")

@admin_bp.route("/term-") #implement term by id
def admin_term():
    classes  = [{"nombre_materia":"calculo IV", "seccion":"N-613", "profesor":"roberto jose", "num_participantes":"30"}, {"nombre_materia":"calculo IV", "seccion":"C-613", "profesor":"roberto jose", "num_participantes":"10"}]
    term = {"nombre":"1-2023"}
    return render_template("admin/adminTerm/term.html", classes=classes, term=term)



