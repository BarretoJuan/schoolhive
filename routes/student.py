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
            return render_template("student/studentDashboard.html", classes=classes, session=session, student = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        return redirect(url_for("login.login"))    

@student_bp.route("/profile", methods = ['GET', 'POST'])
def student_profile():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "student"):
        if request.method == 'GET':
            return render_template("student/studentProfileEdit.html", student = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            # We assume it's a POST
 
            student_email = request.form["email"]
            student_name = request.form["nombre"]
            student_last_name = request.form["apellido"]
            student_cedula = request.form["cedula"]
            student_current_password = request.form["password"]
            student_new_password = request.form["newPassword"]
            student_confirm_password = request.form["confirmarNewPassword"]

            # Check if the new password is written correctly
            if not (student_new_password == student_confirm_password):
                return render_template("student/studentProfileEdit.html", msg = 'Las contraseñas no coinciden', student = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
            # Check if the current password is correct
            hashed_password = hashlib.sha1((student_current_password + current_app.secret_key).encode()).hexdigest()
            query_check_password = "SELECT password FROM estudiante WHERE cedula = %s"
            cursor.execute(query_check_password, (session['cedula'],))
            db_password = cursor.fetchone()

            if hashed_password == db_password['password']:
                # check if the old password is NOT going to be updated
                check_email = """SELECT EXISTS( SELECT 1 FROM estudiante WHERE email = %s) as exist"""
                cursor.execute(check_email, (student_email,))
                email_exist = cursor.fetchone()
                if not student_new_password:
                    
                    if email_exist['exist']:
                        if(student_email == session['email']):
                            query_student_update = """
                            UPDATE estudiante
                            SET nombre = %s, apellido = %s
                            WHERE cedula = %s
                            """
                            cursor.execute(query_student_update,(student_name,student_last_name,student_cedula))
                            mysql.connection.commit()
                        else: 
                            return render_template("student/studentProfileEdit.html", msg = 'El email ya está en uso', student = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})    
                    else:
                        query_student_update = """  
                        UPDATE estudiante
                        SET nombre = %s, apellido = %s, email = %s
                        WHERE cedula = %s
                        """
                        cursor.execute(query_student_update,(student_name,student_last_name, student_email, student_cedula))
                        mysql.connection.commit()
                else:
                    if email_exist['exist']:
                        if(student_email == session['email']):
                            
                            query_student_update = """
                            UPDATE estudiante
                            SET nombre = %s, apellido = %s, password = %s
                            WHERE cedula = %s
                            """
                            new_hashed_password = hashlib.sha1((student_new_password + current_app.secret_key).encode()).hexdigest()
                            cursor.execute(query_student_update,(student_name,student_last_name,new_hashed_password,student_cedula))
                            mysql.connection.commit()
                        else:
                            return render_template("student/studentProfileEdit.html", msg = 'El email ya está en uso', student = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})    
                    else:
                        query_student_update = """
                        UPDATE estudiante
                        SET nombre = %s, apellido = %s, email = %s, password = %s
                        WHERE cedula = %s
                        """
                        new_hashed_password = hashlib.sha1((student_new_password + current_app.secret_key).encode()).hexdigest()
                        cursor.execute(query_student_update,(student_name,student_last_name,student_email,new_hashed_password,student_cedula))
                        mysql.connection.commit()
                
                return redirect(url_for('login.logout'))
            else:
                return render_template("student/studentProfileEdit.html", msg = 'Las contraseña es incorrecta', student = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        return redirect(url_for("login.login"))  


    

