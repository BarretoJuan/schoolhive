from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


#LOGIN ROUTES
@app.route("/")
def route():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("/auth/loginOptions.html")

@app.route("/login/admin")
def login_admin():
    return render_template("/auth/loginAdmin.html")

@app.route("/login/student")
def login_student():
    return render_template("/auth/loginStudent.html")

@app.route("/login/professor")
def login_professor():
    return render_template("/auth/loginProfessor.html")

#ADMIN ROUTES
@app.route("/admin")
def admin():
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/menu")
def admin_dashboard():
    return render_template("admin/adminDashboard.html")

@app.route("/admin/profile")
def admin_profile():
    return render_template("admin/adminProfileEdit.html")

#ADMIN/CLASS ROUTES
@app.route("/admin/class-menu")
def admin_class_menu():
    classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
              {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
    print("classes? ",classes)
    return render_template("admin/adminClass/classMenu.html", classes=classes)

# @app.route("/admin/class-create")
# def admin_class_create():
#     return render_template("admin/adminClass/classCreate.html")

@app.route("/admin/class-assign") #implement major by id
def admin_class_assign():
    classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
              {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("admin/adminClass/classAssign.html",classes=classes, sections=sections, terms=terms)

@app.route("/admin/class-") #implement major by id
def admin_class():
    return render_template("admin/adminClass/class.html")

#ADMIN/MAJOR ROUTES
@app.route("/admin/major-menu")
def admin_major_menu():
    majors=[{"major_name": "Ingenieria informática"}, {"major_name":"ingeniería electrónica"}]
    print("majors? ",majors)
    return render_template("admin/adminMajor/majorMenu.html", majors=majors)

@app.route("/admin/major-create")
def admin_major_create():
    return render_template("admin/adminMajor/majorCreate.html")

@app.route("/admin/major-edit") #implement major by id
def admin_major_edit():
    return render_template("admin/adminMajor/majorEdit.html")

@app.route("/admin/major-") #implement major by id
def admin_major():
    return render_template("admin/adminMajor/major.html")

#ADMIN/PROFESSOR ROUTES
@app.route("/admin/professor-menu")
def admin_professor_menu():
    professors=[{"professor_name": "Ramón Ramírez", "professor_cedula": "10444777"}, {"professor_name":"Jose Jose Sr.", "professor_cedula": "10555777"}]
    print("professors? ",professors)
    return render_template("admin/adminProfessor/professorMenu.html", professors=professors)

@app.route("/admin/professor-create")
def admin_professor_create():
    return render_template("admin/adminProfessor/professorCreate.html")

@app.route("/admin/professor-enroll") #implement professor by id
def admin_professor_enroll():
    classes=[{"class_name":"Cálculo IV"},{"class_name":"Geometría"},{"class_name":"Cálculo III"},{"class_name":"Programación III" }]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("admin/adminProfessor/professorEnroll.html", classes=classes, sections=sections, terms=terms)

@app.route("/admin/professor-") #implement professor by id
def admin_professor():
    classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023"}, {"nombre_materia":"calculo III", "seccion":"n613", "periodo":"1-2023"}]
    professor = {"nombre":"José José", "cedula":"5478487"}
    return render_template("admin/adminProfessor/professor.html", classes=classes, professor=professor)

#ADMIN/SECTION ROUTES
@app.route("/admin/section-menu")
def admin_section_menu():
    sections=[{"section_name": "N-613"}, {"section_name":"C-613"}]
    print("sections? ",sections)
    return render_template("admin/adminSection/sectionMenu.html", sections=sections)

@app.route("/admin/section-create")
def admin_section_create():
    majors = [{"major_name":"ingenieria informatica"},{"major_name":"ingenieria electronica"},{"major_name":"contaduria"}]
    return render_template("admin/adminSection/sectionCreate.html", majors = majors)

@app.route("/admin/section-") #implement section by id
def admin_section():
    classes  = [{"nombre_materia":"calculo IV", "periodo":"1-2023", "profesor":"roberto jose", "num_participantes":"30"}, {"nombre_materia":"calculo IV", "periodo":"1-2023", "profesor":"roberto jose", "num_participantes":"10"}]
    section = {"nombre":"C613", "carrera":"Ingeniería en computación"}
    return render_template("admin/adminSection/section.html", classes=classes, section=section)

#ADMIN/STUDENT ROUTES
@app.route("/admin/student-menu")
def admin_student_menu():
    students=[{"student_name": "Ramón Rodríguez", "student_cedula": "31444777"}, {"student_name":"José José", "student_cedula": "31555777"}]
    
    print("students? ",students)
    return render_template("admin/adminStudent/studentMenu.html", students=students)

@app.route("/admin/student-create")
def admin_student_create():
    return render_template("admin/adminStudent/studentCreate.html")

@app.route("/admin/student-enroll") #implement student by id
def admin_student_enroll():
    classes=[{"class_name":"Cálculo IV"},{"class_name":"Geometría"},{"class_name":"Cálculo III"},{"class_name":"Programación III" }]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("admin/adminStudent/studentEnroll.html", classes=classes, sections=sections, terms=terms)

@app.route("/admin/student-") #implement student by id
def admin_student():
    classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023"}, {"nombre_materia":"calculo III", "seccion":"n613", "periodo":"1-2023"}]
    student = {"nombre":"José José", "cedula":"5478487"}
    return render_template("admin/adminStudent/student.html", classes=classes, student=student)


#ADMIN/TERM ROUTES
@app.route("/admin/term-menu")
def admin_term_menu():
    terms=[{"term_name": "1-2023"}, {"term_name":"2-2023"}]
    print("terms? ",terms)
    return render_template("admin/adminTerm/termMenu.html", terms=terms)

@app.route("/admin/term-create")
def admin_term_create():
    return render_template("admin/adminTerm/termCreate.html")

@app.route("/admin/term-") #implement term by id
def admin_term():
    return render_template("admin/adminMajor/term.html")

#PROFESSOR ROUTES
@app.route("/professor")
def professor():
    return redirect(url_for("professor_dashboard"))

@app.route("/professor/menu")
def professor_dashboard():
    classes=[{"class_name": "Calculo IV", "section_name":"N-613", "term_name":"2-2023", "professor_name":"Roberto Rodriguez", "student_count":"30"},
              {"class_name": "Bases de datos II", "section_name":"C-613", "term_name":"3-2022", "professor_name":"Ramón Rodriguez", "student_count":"15"}]
    sections=[{"section_name":"N-613"},{"section_name":"C-613"},{"section_name":"H-613"},{"section_name":"O-613"}]
    terms=[{"term_name":"1-2023"},{"term_name":"2-2023"},{"term_name":"3-2023"},{"term_name":"3-2022"}]
    return render_template("professor/professorDashboard.html", classes=classes, sections=sections, terms=terms)

@app.route("/professor/profile")
def professor_profile():
    return render_template("professor/professorProfileEdit.html")

@app.route("/professor/class-") #implement id
def professor_class():
    students=[{"name":"roberto roberto", "cedula":"555","nota":"20"},{"name":"pedro roberto", "cedula":"455","nota":"10"},{"name":"ramon roberto", "cedula":"44","nota":"14"},{"name":"enrique roberto", "cedula":"33","nota":"05"}]
    return render_template("professor/professorClass.html", students=students)

#STUDENT ROUTES
@app.route("/student")
def student():
    return redirect(url_for("student_dashboard"))

@app.route("/student/menu")
def student_dashboard():
    classes  = [{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"15"}, {"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"1-2023","profesor":"pedro gomez","cedula_profesor":"5535","nota":"05"},{"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"2-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"20"}, {"nombre_materia":"calculo IV", "seccion":"n613", "periodo":"3-2023","profesor":"pedro gomez","cedula_profesor":"555","nota":"12"}]
    return render_template("student/studentDashboard.html", classes=classes)

@app.route("/student/profile")
def student_profile():
    return render_template("student/studentProfileEdit.html")

#TEST ROUTE

@app.route("/test")
def test():
    return render_template("/admin/adminMajor/majorMenu.html")