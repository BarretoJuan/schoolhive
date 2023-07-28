from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re
from lib.check_user import check_user 

professor_bp = Blueprint("professor", __name__, url_prefix="/professor")

#PROFESSOR ROUTES
@professor_bp.route("/")
def professor():
    return redirect(url_for("professor.professor_dashboard"))

@professor_bp.route("/menu")
def professor_dashboard():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "professor"):
            get_classes = """
              SELECT
            materia.id as class_id,
            materia.nombre as class_name,
            materia.seccion as section_name,
            materia.periodo as term_name,
            COUNT(materia_estudiante.estudiante) as student_count
            from materia
            join materia_estudiante on materia_estudiante.materia = materia.id
            join materia_profesor on materia_profesor.materia = materia.id
            where materia_profesor.profesor = %s
            group by (materia.id)
            order by (materia.periodo)
            """

            cursor.execute(get_classes, (session['cedula'],))
            classes = cursor.fetchall()
            return render_template("professor/professorDashboard.html", classes=classes)

    else:
        return redirect(url_for("login.login"))    
    
    

@professor_bp.route("/profile")
def professor_profile():

    user_check = check_user(session)
    if(user_check == "professor"):
        if request.method == 'GET':
            return render_template("professor/professorProfileEdit.html")
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))    
    

@professor_bp.route("/class/<class_id>/<section_name>/<term_name>", methods = ['GET', 'POST']) # Search by class id, section and term
def professor_class(class_id, section_name, term_name):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    get_students = """
            SELECT 
            estudiante.cedula as cedula,
            estudiante.nombre as name,
            estudiante.apellido as last_name,
            materia_estudiante.nota as nota
            from estudiante
            JOIN materia_estudiante ON materia_estudiante.estudiante = estudiante.cedula
            where materia_estudiante.materia = %s
            order by estudiante.apellido
            """
    cursor.execute(get_students, (class_id,))
    students = cursor.fetchall()
    get_class  = """
            SELECT 
            materia.id as class_id,
            materia.nombre as class_name,
            materia.seccion as class_section,
            materia.periodo as class_term
            from materia
            where materia.id = %s
            """
    cursor.execute(get_class, (class_id))
    class_data = cursor.fetchone()    
    user_check = check_user(session)
    if(user_check == "professor"):
        if request.method == 'GET':
            return render_template("professor/professorClass.html", students=students, class_data = class_data)
        else:
            print(students, "estudiantes?")
            for student in students:
                id_query = "nota_"+str(student['cedula'])
                newGrade = request.form[id_query]
                cursor.execute("UPDATE materia_estudiante SET nota = %s WHERE materia_estudiante.estudiante =%s AND materia_estudiante.materia = %s", (newGrade, student['cedula'], class_id,))
                mysql.connection.commit()
            # User is not admin
            return redirect(url_for("professor.professor_dashboard"))
    else:
        return redirect(url_for("login.login"))    



