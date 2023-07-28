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
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "student"):
            get_classes = """
            SELECT 
            materia.id as id_materia,
            materia.nombre as nombre_materia,
            materia.seccion as seccion,
            materia.periodo as periodo,
            profesor.nombre as profesor,
            profesor.apellido as apellido_profesor,
            profesor.cedula as cedula_profesor,
            materia_estudiante.nota as nota
            from materia
            join materia_profesor on materia_profesor.materia = materia.id
            join materia_estudiante on materia_estudiante.materia = materia.id
            join estudiante on estudiante.cedula = materia_estudiante.estudiante
            join profesor on profesor.cedula = materia_profesor.profesor
            where materia_estudiante.estudiante = %s
            order by materia.periodo, materia.nombre
"""
            cursor.execute(get_classes, (session['cedula'],))
            classes = cursor.fetchall()
            return render_template("student/studentDashboard.html", classes=classes, session=session)
    else:
        return redirect(url_for("login.login"))    

@student_bp.route("/profile", methods = ['GET'])
def student_profile():
    user_check = check_user(session)
    if(user_check == "student"):
        return render_template("student/studentProfileEdit.html")

    else:
        return redirect(url_for("login.login"))  


    

