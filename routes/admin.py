from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re
from lib.check_user import check_user




admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

#ADMIN ROUTES
@admin_bp.route("/")
def admin():
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/menu")
def admin_dashboard():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminDashboard.html", admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))
    

@admin_bp.route("/profile", methods = ['GET','POST'])
def admin_profile():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminProfileEdit.html", admin = {**session, 'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            admin_email = request.form["email"]
            admin_name = request.form["nombre"]
            admin_last_name = request.form["apellido"]
            admin_cedula = request.form["cedula"]
            admin_current_password = request.form["password"]
            admin_new_password = request.form["newPassword"]
            admin_confirm_password = request.form["confirmarNewPassword"]
            
            if not (admin_new_password == admin_confirm_password):
             return render_template("admin/adminProfileEdit.html",msg = "Las contraseñas no coinciden" , admin = {**session,'user_name': session['nombre'] + ' ' + session['apellido']})
            
            # Check if the current password is correct
            hashed_password = hashlib.sha1((admin_current_password + current_app.secret_key).encode()).hexdigest()
            query_check_password = "SELECT password FROM admin WHERE cedula = %s"
            cursor.execute(query_check_password, (session['cedula'],))
            db_password = cursor.fetchone()

            if hashed_password == db_password['password']:
                # check if the old password is NOT going to be updated

                if not admin_new_password:
                    check_email = """SELECT EXISTS( SELECT 1 FROM admin WHERE email = %s) as exist"""
                    cursor.execute(check_email, (admin_email,))
                    email_exist = cursor.fetchone()
                    if email_exist['exist']:
                        if(admin_email == session['email']):
                            query_admin_update = """
                            UPDATE admin
                            SET nombre = %s, apellido = %s
                            WHERE cedula = %s
                            """
                            cursor.execute(query_admin_update,(admin_name,admin_last_name,admin_cedula))
                            mysql.connection.commit()
                        else: 
                            return render_template("admin/adminProfileEdit.html",msg = "El email ya esta en uso" , admin = {**session,'user_name': session['nombre'] + ' ' + session['apellido']})
                    else:
                        query_admin_update = """
                        UPDATE admin
                        SET nombre = %s, apellido = %s, email = %s
                        WHERE cedula = %s
                        """
                        cursor.execute(query_admin_update,(admin_name,admin_last_name,admin_email,admin_cedula))
                        mysql.connection.commit()
                else:
                    check_email = """SELECT EXISTS( SELECT 1 FROM admin WHERE email = %s) as exist"""
                    cursor.execute(check_email, (admin_email,))
                    email_exist = cursor.fetchone()
                    if email_exist['exist']:
                        if (admin_email == session['email']):
                            query_admin_update = """
                            UPDATE admin
                            SET nombre = %s, apellido = %s, password = %s
                            WHERE cedula = %s
                            """
                            new_hashed_password = hashlib.sha1((admin_new_password + current_app.secret_key).encode()).hexdigest()
                            cursor.execute(query_admin_update,(admin_name,admin_last_name,new_hashed_password,admin_cedula))
                            mysql.connection.commit()
                        else:
                            return render_template("admin/adminProfileEdit.html",msg = "El email ya esta en uso" , admin = {**session,'user_name': session['nombre'] + ' ' + session['apellido']})
                    else:
                        query_admin_update = """
                        UPDATE admin
                        SET nombre = %s, apellido = %s, email = %s, password = %s
                        WHERE cedula = %s
                    """
                        new_hashed_password = hashlib.sha1((admin_new_password + current_app.secret_key).encode()).hexdigest()
                        cursor.execute(query_admin_update,(admin_name,admin_last_name,admin_email,new_hashed_password,admin_cedula))
                        mysql.connection.commit()
                
                return redirect(url_for('login.logout'))
            else:
                  return render_template("admin/adminProfileEdit.html",msg = "La contraseña incorrecta" , admin = {**session,'user_name': session['nombre'] + ' ' + session['apellido']})

    else:
        return redirect(url_for("login.login"))
    

#ADMIN/CLASS ROUTES
@admin_bp.route("/class-menu")
def admin_class_menu():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
            get_classes = '''
            SELECT materia.id AS class_id, materia.nombre AS class_name, materia.seccion AS section_name, materia.periodo AS term_name, profesor.nombre AS professor_name, profesor.apellido as professor_last_name, COUNT(materia_estudiante.estudiante) AS student_count 
            FROM materia 
            JOIN materia_profesor 
            ON materia_profesor.materia = materia.id
            JOIN materia_estudiante ON materia_estudiante.materia = materia.id 
            JOIN profesor ON profesor.cedula = materia_profesor.profesor 
            GROUP BY materia_estudiante.materia
            '''
            cursor.execute(get_classes)
            classes = cursor.fetchall()
            return render_template("admin/adminClass/classMenu.html", classes=classes, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        # User is not adming
        return redirect(url_for("login.login"))

@admin_bp.route("/class-assign", methods = ['GET', 'POST']) #implement major by id
def admin_class_assign():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT nombre as section_name from seccion")
    sections = cursor.fetchall()
    cursor.execute("SELECT nombre as term_name from periodo")
    terms = cursor.fetchall()       
    log_msg="" 
    user_check = check_user(session)

    if(user_check == "admin"):
        if request.method == 'GET':       
            return render_template("admin/adminClass/classAssign.html", sections=sections, terms=terms, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            class_name = request.form['nombreMateria']
            class_section = request.form['seccion']
            class_term = request.form['periodo']

            check_class = "SELECT EXISTS (SELECT 1 FROM materia WHERE nombre = %s AND seccion = %s AND periodo = %s) AS exist"
            cursor.execute(check_class, (class_name, class_section, class_term,))
            class_exists = cursor.fetchone()
            print("/ ", class_exists['exist'])
            

            if not class_exists["exist"]:
                query = "INSERT INTO materia (nombre, seccion, periodo) VALUES (%s,%s,%s)"
                cursor.execute(query, (class_name, class_section, class_term,))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_class_menu"))
            else:
                log_msg = "Esta materia ya existe."
                return render_template("admin/adminClass/classAssign.html", sections=sections, terms=terms, msg=log_msg, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        # User is not admin
        return redirect(url_for("login.login"))
   
    

@admin_bp.route("/class/<id>") #implement major by id
def admin_class(id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            get_class_data = """
            SELECT materia.nombre as nombre,
            materia.id as id,
            materia.periodo as periodo,
            materia.seccion as seccion,
            profesor.nombre as profesor,
            profesor.apellido as profesor_apellido
            from materia
            join materia_profesor on materia_profesor.materia = materia.id
            join profesor on profesor.cedula = materia_profesor.profesor
            where materia = %s
            """
            cursor.execute(get_class_data, (id,))
            class_data = cursor.fetchone()

            get_student_data = '''
            SELECT 
            estudiante.nombre as nombre,
            estudiante.cedula as cedula,
            estudiante.apellido as apellido
            from estudiante
            join materia_estudiante on materia_estudiante.estudiante = estudiante.cedula
            where materia_estudiante.materia = %s
            order by estudiante.apellido
'''

            cursor.execute(get_student_data, (id,))
            students = cursor.fetchall()
            return render_template("admin/adminClass/class.html", class_data=class_data, students=students, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        return redirect(url_for("login.login"))
    
    

#ADMIN/MAJOR ROUTES
@admin_bp.route("/major-menu")
def admin_major_menu():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
            cursor.execute("SELECT nombre AS major_name FROM carrera")
            majors = cursor.fetchall() 
            return render_template("admin/adminMajor/majorMenu.html", majors=majors, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        return redirect(url_for("login.login"))

@admin_bp.route("/major-create", methods = ['GET', 'POST'])
def admin_major_create():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    log_msg = ''
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminMajor/majorCreate.html", admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else: # We assume they cannot send any other method but post
            major_name = request.form['nombreCarrera']
            query_major_exist = "SELECT EXISTS(SELECT 1 FROM carrera WHERE nombre = %s) AS exist"
            cursor.execute(query_major_exist, (major_name,))
            check_major_exist = cursor.fetchone()

            if not check_major_exist['exist']:
                cursor.execute("INSERT INTO carrera (nombre) VALUES (%s)", (major_name,))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_major_menu"))
            else:
               log_msg = "Esta carrera ya existe" # It already exist
               return render_template("admin/adminMajor/majorCreate.html", msg = log_msg, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
            
    else:
        # User is not admin
        return redirect(url_for("login.login"))    
    

    

@admin_bp.route("/major/<name>") #implement major by id
def admin_major(name):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            cursor.execute("SELECT nombre as nombre from carrera where nombre = %s", (name,))
            major = cursor.fetchone()

            get_student_data = """
            SELECT
            estudiante.nombre as nombre,
            estudiante.apellido as apellido,
            estudiante.cedula as cedula,
            estudiante.carrera as carrera
            from estudiante
            join carrera on carrera.nombre = estudiante.carrera
            where carrera.nombre = %s
            order by estudiante.apellido
"""
            cursor.execute(get_student_data, (name,))
            students=cursor.fetchall()

            get_classes_data = '''
            SELECT
            materia.nombre as nombre,
            materia.seccion as seccion,
            materia.periodo as periodo,
            profesor.nombre as profesor,
            profesor.apellido as profesor_apellido,
            profesor.cedula as cedula_profesor,
            COUNT(materia_estudiante.estudiante) as num_participantes
            from materia
            join materia_profesor on materia_profesor.materia = materia.id
            join materia_estudiante on materia_estudiante.materia = materia.id
            join profesor on profesor.cedula = materia_profesor.profesor
            join seccion on seccion.nombre = materia.seccion
            where seccion.carrera = %s
            group by materia_estudiante.materia
            order by materia.periodo
            
'''
            cursor.execute(get_classes_data, (name,))
            classes = cursor.fetchall()
            return render_template("admin/adminMajor/major.html", major=major,students=students,classes=classes, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        return redirect(url_for("login.login"))   

#ADMIN/PROFESSOR ROUTES
@admin_bp.route("/professor-menu", methods = ['GET'])
def admin_professor_menu():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
            get_professors = """SELECT 
            nombre AS professor_name,
            apellido AS professor_last_name,
            cedula AS professor_cedula
            FROM profesor"""
            cursor.execute(get_professors)
            professors=cursor.fetchall()

            return render_template("admin/adminProfessor/professorMenu.html", professors=professors, admin = {'user_name': session['nombre'] + ' ' + session['apellido']} )
    else:
        return redirect(url_for("login.login"))   
    

@admin_bp.route("/professor-create", methods=["GET", "POST"])
def admin_professor_create():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    log_msg = ''
    error_flag = False
    user_check = check_user(session)

    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminProfessor/professorCreate.html", admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            professor_name = request.form["nombre"]
            professor_last_name = request.form["apellido"]
            professor_id = request.form["cedula"]
            professor_email = request.form["email"]
            professor_password = request.form["password"]
            professor_confirm_password = request.form["confirmarPassword"]
            professor_hash = hashlib.sha1((professor_password + current_app.secret_key).encode()).hexdigest()
            
            cursor.execute("SELECT EXISTS (SELECT 1 FROM profesor WHERE cedula = %s) AS exist", (professor_id,))
            cedula_exists = cursor.fetchone()
            if cedula_exists['exist']:
                log_msg = "Esta cédula ya está en uso."
                error_flag = True 

        
            cursor.execute("SELECT EXISTS (SELECT 1 FROM profesor WHERE email = %s) AS exist", (professor_email,))

            email_exists = cursor.fetchone()
            if email_exists['exist']:
                log_msg = "Este email ya está en uso."
                error_flag = True 
            
            if professor_password != professor_confirm_password:
                log_msg = "Las contraseñas no coinciden." 
                error_flag = True 

            if error_flag:
                return render_template("admin/adminProfessor/professorCreate.html", msg = log_msg, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
            else:
                insert_professor = "INSERT INTO profesor(cedula, nombre, apellido, email, password) VALUES(%s, %s, %s, %s, %s)"
                cursor.execute(insert_professor, (professor_id, professor_name, professor_last_name, professor_email, professor_hash))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_professor_menu"))

    else:
        return redirect(url_for("login.login"))

@admin_bp.route("/professor-enroll/<cedula>", methods = ['GET', 'POST']) #implement professor by id
def admin_professor_enroll(cedula):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # SELECT id, nombre FROM materia WHERE NOT EXISTS(SELECT materia FROM materia_profesor WHERE materia.id = materia_profesor.materia);
    get_classes = " SELECT id as class_id, nombre as class_name, periodo as class_term, seccion as class_section FROM materia WHERE NOT EXISTS(SELECT materia FROM materia_profesor WHERE materia.id = materia_profesor.materia)"
    cursor.execute(get_classes)
    classes=cursor.fetchall()
    get_professor = "SELECT cedula as professor_cedula, nombre as professor_name, apellido as professor_last_name from profesor where cedula = %s"
    cursor.execute (get_professor, (cedula,))
    professor=cursor.fetchone()
    log_msg=""
    user_check = check_user(session)

    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminProfessor/professorEnroll.html", classes=classes, professor=professor, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            class_id = request.form["materia"]
            check_if_class_has_professor = "SELECT EXISTS (SELECT 1 FROM materia_profesor WHERE materia = %s) AS exist"
            cursor.execute(check_if_class_has_professor, (class_id),)
            professor_check = cursor.fetchone()

            if not professor_check['exist']:
                cursor.execute ("INSERT INTO materia_profesor (materia, profesor) VALUES (%s,%s)", (class_id,cedula,))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_professor_menu"))
            else:
                log_msg="Esta materia ya tiene un profesor asignado." 
                return render_template("admin/adminProfessor/professorEnroll.html", classes=classes, professor=professor,msg=log_msg)
            
    else:
        return redirect(url_for("login.login"))   

@admin_bp.route("/professor/<cedula>") #implement professor by id
def admin_professor(cedula):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            get_classes = """
            SELECT materia.id AS id_materia,
            materia.nombre AS nombre_materia,
            materia.seccion AS seccion,
            materia.periodo AS periodo
            FROM materia
            INNER JOIN materia_profesor ON materia_profesor.materia = materia.id
            WHERE materia_profesor.profesor = %s
            ORDER BY materia.periodo
            """
            cursor.execute(get_classes, (cedula,))
            classes = cursor.fetchall()

            get_professor = " SELECT nombre as nombre, cedula as cedula, apellido as apellido FROM profesor where cedula = %s"
            
            cursor.execute(get_professor, (cedula,))
            professor=cursor.fetchone()

            return render_template("admin/adminProfessor/professor.html", classes=classes, professor=professor, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        # User is not admin
        return redirect(url_for("login.login"))
    

#ADMIN/SECTION ROUTES
@admin_bp.route("/section-menu")
def admin_section_menu():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            get_sections = "SELECT nombre as section_name FROM seccion"
            cursor.execute(get_sections)
            sections = cursor.fetchall()
            return render_template("admin/adminSection/sectionMenu.html", sections=sections, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))  

@admin_bp.route("/section-create", methods = ['GET', 'POST'])
def admin_section_create():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    log_msg=""
    get_majors = "SELECT nombre as major_name FROM carrera"
    cursor.execute(get_majors)
    majors = cursor.fetchall()
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminSection/sectionCreate.html", majors = majors, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            section_name = request.form["nombreSeccion"]
            section_major = request.form["carrera"]
            query_section_exists = "SELECT EXISTS (SELECT 1 FROM seccion WHERE nombre = %s) AS exist"
            cursor.execute(query_section_exists, (section_name,))
            section_exists = cursor.fetchone()
            if section_exists['exist'] == 0:
                insert_section = "INSERT INTO seccion(nombre, carrera) VALUES (%s, %s)"
                cursor.execute(insert_section, (section_name, section_major))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_section_menu"))
            else:
                log_msg = "Esta sección ya existe."
                return render_template("admin/adminSection/sectionCreate.html", majors = majors, msg=log_msg, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})

    else:
        # User is not admin
        return redirect(url_for("login.login"))  


@admin_bp.route("/section/<section_name>") #implement section by id
def admin_section(section_name):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            get_classes ='''
                SELECT 
                materia.seccion as seccion,
                materia.id AS materia_id,
                materia.nombre AS nombre_materia,
                materia.periodo AS periodo,
                profesor.nombre AS profesor,
                profesor.apellido as profesor_apellido,   
                COUNT(materia_estudiante.estudiante) AS num_participantes
                FROM materia
                JOIN materia_profesor ON materia.id = materia_profesor.materia
                JOIN profesor ON materia_profesor.profesor = profesor.cedula
                JOIN materia_estudiante ON materia.id = materia_estudiante.materia
                where materia.seccion = %s 
                GROUP BY materia.id, materia.nombre, materia.periodo, profesor.nombre
                ORDER BY materia.periodo;


                        
            ''' 
            cursor.execute (get_classes, (section_name,))
            classes = cursor.fetchall()

            get_section = "select nombre as nombre, carrera as carrera from seccion where nombre = %s"
            cursor.execute(get_section, (section_name,))
            section = cursor.fetchone()
            return render_template("admin/adminSection/section.html", classes=classes, section=section, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        return redirect(url_for("login.login"))  

#ADMIN/STUDENT ROUTES
@admin_bp.route("/student-menu")
def admin_student_menu():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        get_students = "SELECT nombre as student_name, apellido as student_last_name, cedula as student_cedula from estudiante"
        cursor.execute(get_students)
        students = cursor.fetchall()
        return render_template("admin/adminStudent/studentMenu.html", students=students, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})     
       
    else:
        return redirect(url_for("login.login"))  

@admin_bp.route("/student-create", methods=['GET', 'POST'])
def admin_student_create():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    log_msg = ''
    error_flag = False
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            get_majors = '''
            SELECT nombre as major_name FROM carrera
            '''
            cursor.execute(get_majors)
            majors=cursor.fetchall()
            return render_template("admin/adminStudent/studentCreate.html", majors=majors, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
              
        elif request.method == 'POST':
            student_name = request.form["nombre"]
            student_last_name = request.form["apellido"]
            student_id = request.form["cedula"]
            student_major = request.form["carrera"]
            student_email = request.form["email"]
            student_password = request.form["password"]
            student_confirm_password = request.form["confirmarPassword"]
            student_hash = hashlib.sha1((student_password + current_app.secret_key).encode()).hexdigest()
            
            cursor.execute("SELECT EXISTS (SELECT 1 FROM estudiante WHERE cedula = %s) AS exist", (student_id,))
            cedula_exists = cursor.fetchone()

            if cedula_exists['exist'] == 1:
                log_msg = "Esta cédula ya está en uso."
                error_flag = True 
    
            cursor.execute("SELECT EXISTS (SELECT 1 FROM estudiante WHERE email = %s) AS exist", (student_email,))
            email_exists = cursor.fetchone()
            if email_exists['exist'] == 1:
                log_msg = "Este email ya está en uso."
                error_flag = True 
            
            if student_password != student_confirm_password:
                log_msg = "Las contraseñas no coinciden." 
                error_flag = True 

            if error_flag:
                return render_template("admin/adminStudent/studentCreate.html", msg = log_msg, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
            else:
                insert_student = "INSERT INTO estudiante(cedula, nombre, apellido, email, password, carrera) VALUES(%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_student, (student_id, student_name, student_last_name, student_email, student_hash, student_major))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_student_menu"))

        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login")) 

@admin_bp.route("/student-enroll/<cedula>", methods = ['GET', 'POST']) #implement student by id
def admin_student_enroll(cedula):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT nombre as student_name, apellido as student_last_name, cedula as student_cedula from estudiante where cedula = %s", (cedula,))
    student = cursor.fetchone()
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':

            get_classes = "SELECT id AS class_id, seccion as class_section, periodo as class_term, nombre as class_name FROM materia WHERE NOT EXISTS(SELECT materia FROM materia_estudiante WHERE materia.id = materia_estudiante.materia AND materia_estudiante.estudiante = %s)"
            cursor.execute(get_classes, (cedula,))
            classes = cursor.fetchall()
            return render_template("admin/adminStudent/studentEnroll.html", classes=classes, student=student, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            # Assuming POST method
            class_id = request.form['materia']
            enroll_student = "INSERT INTO materia_estudiante (materia, estudiante, nota) VALUES (%s,%s, 0)"
            cursor.execute(enroll_student, (class_id, cedula,))
            mysql.connection.commit()
            return redirect(url_for("admin.admin_student_menu"))
    else:
        return redirect(url_for("login.login")) 

@admin_bp.route("/student/<cedula>")
def admin_student(cedula):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if user_check == "admin":
        if request.method == 'GET':
            get_student = "SELECT nombre, apellido, cedula FROM estudiante WHERE cedula = %s"
            cursor.execute(get_student, (cedula,))
            student = cursor.fetchone()
            get_classes = '''
                SELECT 
                materia_estudiante.estudiante,
                materia.nombre as nombre_materia,
                materia.seccion as seccion,
                materia.periodo as periodo,
                materia_estudiante.nota as nota
                FROM materia
                INNER JOIN materia_estudiante ON materia_estudiante.materia = materia.id
                WHERE materia_estudiante.estudiante = %s
                ORDER BY materia.periodo
            '''
            cursor.execute(get_classes, (cedula,))
            classes = cursor.fetchall()
        return render_template("admin/adminStudent/student.html", student=student, classes=classes, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})

        
    else:
        return redirect(url_for("login.login"))

#ADMIN/TERM ROUTES
@admin_bp.route("/term-menu", methods = ['GET'])
def admin_term_menu():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
            get_terms = "SELECT nombre as term_name FROM periodo"
            cursor.execute(get_terms)
            terms = cursor.fetchall()
            return render_template("admin/adminTerm/termMenu.html", terms=terms, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        return redirect(url_for("login.login")) 

@admin_bp.route("/term-create", methods = ['GET', "POST"])
def admin_term_create():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminTerm/termCreate.html", admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            term_number = request.form['numPeriodo']
            term_year = request.form['yearPeriodo']
            term_name = term_number+"-"+term_year

            check_term_exist = "SELECT EXISTS (SELECT 1 FROM periodo WHERE nombre = %s ) AS exist"
            cursor.execute(check_term_exist, (term_name,))
            term = cursor.fetchone()

            if not term['exist']:
                insert_term = "INSERT INTO periodo (nombre) VALUES (%s)"
                cursor.execute(insert_term, (term_name,))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_term_menu"))
            else:
                return render_template("admin/adminTerm/termCreate.html", msg = "Ya este período existe", admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
    else:
        # User is not admin
        return redirect(url_for("login.login")) 

@admin_bp.route("/term/<name>") #implement term by id
def admin_term(name):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            cursor.execute ("SELECT periodo.nombre as nombre from periodo where periodo.nombre = %s", (name,))
            term = cursor.fetchone()

            get_classes = '''
                SELECT 
            materia.periodo as periodo,
            materia.id AS materia_id,
            materia.nombre AS nombre_materia,
            materia.seccion AS seccion,
            profesor.nombre AS profesor,
            profesor.apellido as profesor_apellido,   
            COUNT(materia_estudiante.estudiante) AS num_participantes
            FROM materia
            JOIN materia_profesor ON materia.id = materia_profesor.materia
            JOIN profesor ON materia_profesor.profesor = profesor.cedula
            JOIN materia_estudiante ON materia.id = materia_estudiante.materia
            where materia.periodo = %s 
            GROUP BY materia.id, materia.nombre, materia.periodo, profesor.nombre
            ORDER BY materia.seccion;

'''         
            cursor.execute(get_classes, (name,))
            classes = cursor.fetchall()
            return render_template("admin/adminTerm/term.html", classes=classes, term=term, admin = {'user_name': session['nombre'] + ' ' + session['apellido']})
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login")) 



