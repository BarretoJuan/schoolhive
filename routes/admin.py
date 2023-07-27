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
            return render_template("admin/adminDashboard.html")
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))
    

@admin_bp.route("/profile")
def admin_profile():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminProfileEdit.html")
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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
            SELECT materia.nombre AS class_name, materia.seccion AS section_name, materia.periodo AS term_name, profesor.nombre AS professor_name, COUNT(materia_estudiante.estudiante) AS student_count 
            FROM materia 
            JOIN materia_profesor 
            ON materia_profesor.materia = materia.id
            JOIN materia_estudiante ON materia_estudiante.materia = materia.id 
            JOIN profesor ON profesor.cedula = materia_profesor.profesor 
            GROUP BY materia_estudiante.materia
            '''
            

            cursor.execute(get_classes)
            classes = cursor.fetchall()
            return render_template("admin/adminClass/classMenu.html", classes=classes)
    else:
        # User is not adminf
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
            return render_template("admin/adminClass/classAssign.html", sections=sections, terms=terms)
        else:
            class_name = request.form['nombreMateria']
            class_section = request.form['seccion']
            class_term = request.form['periodo']

            check_class = "SELECT EXISTS (SELECT 1 FROM materia WHERE nombre = %s AND seccion = %s AND periodo = %s) AS exist"
            cursor.execute(check_class, (class_name, class_section, class_term,))
            class_exists = cursor.fetchone()

            if not class_exists["exist"]:
                query = "INSERT INTO materia (nombre, seccion, periodo) VALUES (%s,%s,%s)"
                cursor.execute(query, (class_name, class_section, class_term,))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_class_menu"))
            else:
                log_msg = "Esta materia ya existe."
                return render_template("admin/adminClass/classAssign.html", sections=sections, terms=terms, msg=log_msg)
    else:
        # User is not admin
        return redirect(url_for("login.login"))
   
    

@admin_bp.route("/class-") #implement major by id
def admin_class():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classs = {"nombre":"Calculo IV", "periodo":"1-2023","seccion":"n-613","profesor":"jose jose"}
            students = [{"nombre":"student1", "cedula":"5566"},{"nombre":"student2", "cedula":"55466"}]
            return render_template("admin/adminClass/class.html", classs=classs, students=students)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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
            print("majors? ",majors)
            return render_template("admin/adminMajor/majorMenu.html", majors=majors)
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
            return render_template("admin/adminMajor/majorCreate.html")
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
               return render_template("admin/adminMajor/majorCreate.html", msg = log_msg)
            
    else:
        # User is not admin
        return redirect(url_for("login.login"))    
    

    

@admin_bp.route("/major-") #implement major by id
def admin_major():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            major={"nombre":"Ingenieria informática"}
            students=[{"nombre":"roberto roberto", "cedula":"555"},{"nombre":"pedro roberto", "cedula":"455"},{"nombre":"ramon roberto", "cedula":"44"},{"nombre":"enrique roberto", "cedula":"33"}]
            classes=[{"nombre":"calculo IV", "periodo":"1-2023", "seccion":"n-613", "profesor":"roberto jose", "cedula_profesor":"5533", "num_participantes":"30"}, {"nombre":"calculo IV", "periodo":"1-2023", "seccion":"n-613", "profesor":"roberto jose", "cedula_profesor":"5533", "num_participantes":"30"}]
            return render_template("admin/adminMajor/major.html", major=major,students=students,classes=classes)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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

            return render_template("admin/adminProfessor/professorMenu.html", professors=professors)
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
            return render_template("admin/adminProfessor/professorCreate.html")
        elif request.method == 'POST':
            professor_name = request.form["nombre"]
            professor_last_name = request.form["apellido"]
            professor_id = request.form["cedula"]
            professor_email = request.form["email"]
            professor_password = request.form["password"]
            professor_confirm_password = request.form["confirmarPassword"]
            professor_hash = hashlib.sha1((professor_password + current_app.secret_key).encode()).hexdigest()
            
            cursor.execute("SELECT EXISTS (SELECT 1 FROM profesor WHERE cedula = %s) AS exist", (professor_id,))
            cedula_exists = cursor.fetchone()

            if cedula_exists['exist'] == 1:
                log_msg = "Esta cédula ya está en uso."
                error_flag = True 
    
            cursor.execute("SELECT EXISTS (SELECT 1 FROM profesor WHERE email = %s) AS exist", (professor_id,))
            email_exists = cursor.fetchone()
            if email_exists['exist'] == 1:
                log_msg = "Este email ya está en uso."
                error_flag = True 
            
            if professor_password != professor_confirm_password:
                log_msg = "Las contraseñas no coinciden." 
                error_flag = True 

            if error_flag:
                return render_template("admin/adminProfessor/professorCreate.html", msg = log_msg)
            else:
                insert_professor = "INSERT INTO profesor(cedula, nombre, apellido, email, password) VALUES(%s, %s, %s, %s, %s)"
                cursor.execute(insert_professor, (professor_id, professor_name, professor_last_name, professor_email, professor_hash))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_professor_menu"))
        else:
            # User is not admin
            return redirect(url_for("login.login"))

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
            return render_template("admin/adminProfessor/professorEnroll.html", classes=classes, professor=professor)
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

@admin_bp.route("/professor-") #implement professor by id
def admin_professor():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023"}, {"nombre_materia":"calculo III", "seccion":"n613", "periodo":"1-2023"}]
            professor = {"nombre":"José José", "cedula":"5478487"}
            return render_template("admin/adminProfessor/professor.html", classes=classes, professor=professor)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
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
            return render_template("admin/adminSection/sectionMenu.html", sections=sections)
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
            return render_template("admin/adminSection/sectionCreate.html", majors = majors)
        else:
            section_name = request.form["nombreSeccion"]
            section_major = request.form["carrera"]
            query_section_exists = "SELECT EXISTS (SELECT 1 FROM seccion WHERE nombre = %s) AS exist"
            cursor.execute(query_section_exists, (section_name,))
            section_exists = cursor.fetchone()
            if not section_exists['exist']:
                insert_section = "INSERT INTO seccion(nombre, carrera) VALUES (%s, %s)"
                cursor.execute(insert_section, (section_name, section_major))
                mysql.connection.commit()
                return redirect(url_for("admin.admin_section_menu"))
            else:
                log_msg = "Esta sección ya existe."
                return render_template("admin/adminSection/sectionCreate.html", majors = majors, msg=log_msg)

    else:
        # User is not admin
        return redirect(url_for("login.login"))  


@admin_bp.route("/section-") #implement section by id
def admin_section():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes  = [{"nombre_materia":"calculo IV", "periodo":"1-2023", "profesor":"roberto jose", "num_participantes":"30"}, {"nombre_materia":"calculo IV", "periodo":"1-2023", "profesor":"roberto jose", "num_participantes":"10"}]
            section = {"nombre":"C613", "carrera":"Ingeniería en computación"}
            return render_template("admin/adminSection/section.html", classes=classes, section=section)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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
        return render_template("admin/adminStudent/studentMenu.html", students=students)     
       
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
            return render_template("admin/adminStudent/studentCreate.html", majors=majors)
              
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
    
            cursor.execute("SELECT EXISTS (SELECT 1 FROM estudiante WHERE email = %s) AS exist", (student_id,))
            email_exists = cursor.fetchone()
            if email_exists['exist'] == 1:
                log_msg = "Este email ya está en uso."
                error_flag = True 
            
            if student_password != student_confirm_password:
                log_msg = "Las contraseñas no coinciden." 
                error_flag = True 

            if error_flag:
                return render_template("admin/adminStudent/studentCreate.html", msg = log_msg)
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
            return render_template("admin/adminStudent/studentEnroll.html", classes=classes, student=student)
        else:
            # Assuming POST method
            class_id = request.form['materia']
            enroll_student = "INSERT INTO materia_estudiante (materia, estudiante) VALUES (%s,%s)"
            cursor.execute(enroll_student, (class_id, cedula,))
            mysql.connection.commit()
            return redirect(url_for("admin.admin_student_menu"))
    else:
        return redirect(url_for("login.login")) 
    

@admin_bp.route("/student-") #implement student by id
def admin_student():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023"}, {"nombre_materia":"calculo III", "seccion":"n613", "periodo":"1-2023"}]
            student = {"nombre":"José José", "cedula":"5478487"}
            return render_template("admin/adminStudent/student.html", classes=classes, student=student)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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
            return render_template("admin/adminTerm/termMenu.html", terms=terms)
    else:
        return redirect(url_for("login.login")) 

@admin_bp.route("/term-create", methods = ['GET', "POST"])
def admin_term_create():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminTerm/termCreate.html")
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
                return render_template("admin/adminTerm/termCreate.html", msg = "Ya este período existe")
    else:
        # User is not admin
        return redirect(url_for("login.login")) 

@admin_bp.route("/term-") #implement term by id
def admin_term():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes  = [{"nombre_materia":"calculo IV", "seccion":"N-613", "profesor":"roberto jose", "num_participantes":"30"}, {"nombre_materia":"calculo IV", "seccion":"C-613", "profesor":"roberto jose", "num_participantes":"10"}]
            term = {"nombre":"1-2023"}
            return render_template("admin/adminTerm/term.html", classes=classes, term=term)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login")) 



