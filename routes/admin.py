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
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
            {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
            print("classes? ",classes)
            return render_template("admin/adminClass/classMenu.html", classes=classes)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))

@admin_bp.route("/class-assign") #implement major by id
def admin_class_assign():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
            {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
            sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
            terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
            return render_template("admin/adminClass/classAssign.html",classes=classes, sections=sections, terms=terms)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
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
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            majors=[{"major_name": "Ingenieria informática"}, {"major_name":"ingeniería electrónica"}]
            print("majors? ",majors)
            return render_template("admin/adminMajor/majorMenu.html", majors=majors)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))

@admin_bp.route("/major-create")
def admin_major_create():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminMajor/majorCreate.html")
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))    
    

@admin_bp.route("/major-edit") #implement major by id
def admin_major_edit():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminMajor/majorEdit.html")
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
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
@admin_bp.route("/professor-menu")
def admin_professor_menu():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            professors=[{"professor_name": "Ramón Ramírez", "professor_cedula": "10444777"}, {"professor_name":"Jose Jose Sr.", "professor_cedula": "10555777"}]
            print("professors? ",professors)
            return render_template("admin/adminProfessor/professorMenu.html", professors=professors)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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

@admin_bp.route("/professor-enroll") #implement professor by id
def admin_professor_enroll():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes=[{"class_name":"Cálculo IV"},{"class_name":"Geometría"},{"class_name":"Cálculo III"},{"class_name":"Programación III" }]
            sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
            terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
            return render_template("admin/adminProfessor/professorEnroll.html", classes=classes, sections=sections, terms=terms)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            sections=[{"section_name": "N-613"}, {"section_name":"C-613"}]
            print("sections? ",sections)
            return render_template("admin/adminSection/sectionMenu.html", sections=sections)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))  

@admin_bp.route("/section-create")
def admin_section_create():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            majors = [{"major_name":"ingenieria informatica"},{"major_name":"ingenieria electronica"},{"major_name":"contaduria"}]
            return render_template("admin/adminSection/sectionCreate.html", majors = majors)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
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
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            students=[{"student_name": "Ramón Rodríguez", "student_cedula": "31444777"}, {"student_name":"José José", "student_cedula": "31555777"}]
            print("students? ",students)
            return render_template("admin/adminStudent/studentMenu.html", students=students)     
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login"))  

@admin_bp.route("/student-create")
def admin_student_create():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminStudent/studentCreate.html")   
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login")) 

@admin_bp.route("/student-enroll") #implement student by id
def admin_student_enroll():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            classes=[{"class_name":"Cálculo IV"},{"class_name":"Geometría"},{"class_name":"Cálculo III"},{"class_name":"Programación III" }]
            sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
            terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
            return render_template("admin/adminStudent/studentEnroll.html", classes=classes, sections=sections, terms=terms)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
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
@admin_bp.route("/term-menu")
def admin_term_menu():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            terms=[{"term_name": "1-2023"}, {"term_name":"2-2023"}]
            print("terms? ",terms)
            return render_template("admin/adminTerm/termMenu.html", terms=terms)
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
        return redirect(url_for("login.login")) 

@admin_bp.route("/term-create")
def admin_term_create():
    user_check = check_user(session)
    if(user_check == "admin"):
        if request.method == 'GET':
            return render_template("admin/adminTerm/termCreate.html")
        else:
            # User is not admin
            return redirect(url_for("login.login"))
    else:
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



