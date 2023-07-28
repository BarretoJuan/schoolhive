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
            return render_template("professor/professorDashboard.html", classes=classes, professor = {'user_name': session['nombre'] + ' ' + session['apellido']})

    else:
        return redirect(url_for("login.login"))    
    
    

@professor_bp.route("/profile", methods =['GET','POST'])
def professor_profile():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "professor"):
        if request.method == 'GET':
            return render_template("professor/professorProfileEdit.html", professor = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            # We assume it's a POST
 
            professor_email = request.form["email"]
            professor_name = request.form["nombre"]
            professor_last_name = request.form["apellido"]
            professor_cedula = request.form["cedula"]
            professor_current_password = request.form["password"]
            professor_new_password = request.form["newPassword"]
            professor_confirm_password = request.form["confirmarNewPassword"]

            # Check if the new password is written correctly
            if not (professor_new_password == professor_confirm_password):
                return render_template("professor/professorProfileEdit.html", msg = 'Las contraseñas no coinciden', professor = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
            # Check if the current password is correct
            hashed_password = hashlib.sha1((professor_current_password + current_app.secret_key).encode()).hexdigest()
            query_check_password = "SELECT password FROM profesor WHERE cedula = %s"
            cursor.execute(query_check_password, (session['cedula'],))
            db_password = cursor.fetchone()

            if hashed_password == db_password['password']:
                # check if the old password is NOT going to be updated

                if not professor_new_password:
                    check_email = """SELECT EXISTS( SELECT 1 FROM profesor WHERE email = %s) as exist"""
                    cursor.execute(check_email, (professor_email,))
                    email_exist = cursor.fetchone()
                    if not email_exist['exist']:
                        if professor_email == session['email']:
                            query = """
                            UPDATE profesor
                            SET nombre = %s, apellido = %s WHERE cedula =%s"""
                            cursor.execute(query, (professor_name, professor_last_name,))
                            mysql.connection.commit()
                        else:
                            return render_template("professor/professorProfileEdit.html", msg="este email ya esta en uso", professor = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
                    else:
                        query_professor_update = """
                        UPDATE profesor
                        SET nombre = %s, apellido = %s, email = %s
                        WHERE cedula = %s
                        """
                        cursor.execute(query_professor_update,(professor_name,professor_last_name,professor_email,professor_cedula))
                        mysql.connection.commit()
                else:
                    check_email = """SELECT EXISTS( SELECT 1 FROM profesor WHERE email = %s) as exist"""
                    cursor.execute(check_email, (professor_email,))
                    email_exist = cursor.fetchone()
                    if email_exist['exist']:
                        if(professor_email == session['email']):

                            query = """
                            UPDATE profesor
                            SET nombre = %s, apellido = %s, password = %s WHERE cedula =%s"""
                            new_hashed_password = hashlib.sha1((professor_new_password + current_app.secret_key).encode()).hexdigest()
                            cursor.execute(query, (professor_name, professor_last_name,new_hashed_password, professor_cedula))
                            mysql.connection.commit()
                        else: 
                            return render_template("professor/professorProfileEdit.html", msg="este email ya esta en uso", professor = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
                    else:
                        query_professor_update = """
                        UPDATE profesor
                        SET nombre = %s, apellido = %s, email = %s, password = %s
                        WHERE cedula = %s
                        """
                        new_hashed_password = hashlib.sha1((professor_new_password + current_app.secret_key).encode()).hexdigest()
                        cursor.execute(query_professor_update,(professor_name,professor_last_name,professor_email,new_hashed_password,professor_cedula))
                        mysql.connection.commit()
                
                return redirect(url_for('login.logout'))
            else:
                return render_template("professor/professorProfileEdit.html", msg = 'La contraseña es incorrecta', professor = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
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
            return render_template("professor/professorClass.html", students=students, class_data = class_data,  professor = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            for student in students:
                id_query = "nota_"+str(student['cedula'])
                newGrade = request.form[id_query]
                cursor.execute("UPDATE materia_estudiante SET nota = %s WHERE materia_estudiante.estudiante =%s AND materia_estudiante.materia = %s", (newGrade, student['cedula'], class_id,))
                mysql.connection.commit()

            return redirect(url_for("professor.professor_class", class_id=class_id, section_name=section_name, term_name=term_name))
    else:
        return redirect(url_for("login.login"))    

@professor_bp.route("/classForm/<class_id>")
def professor_form(class_id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    user_check = check_user(session)
    get_class_data = '''
    SELECT 
    materia.nombre as nombre,
    materia.id as id,
    materia.periodo as periodo,
    materia.seccion as seccion
    from materia
    where materia.id = %s
    '''
    cursor.execute(get_class_data, (class_id,))
    class_data = cursor.fetchone()

    get_students_data = """
    SELECT 
    estudiante.cedula as cedula,
    estudiante.nombre as nombre,
    estudiante.apellido as apellido,
    materia_estudiante.nota as nota
    from estudiante
    join materia_estudiante on materia_estudiante.estudiante = estudiante.cedula
    where materia_estudiante.materia = %s
    order by estudiante.apellido, estudiante.cedula
    """
    cursor.execute(get_students_data, (class_id,))
    students = cursor.fetchall()
    if(user_check == "professor"):
        return render_template("professor/professorTable.html", session = session, class_data=class_data, students=students )
    else:
        return redirect(url_for("login.login"))    





