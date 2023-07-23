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

#ADMIN/MAJOR ROUTES
@app.route("/admin/major-menu")
def admin_major_menu():
    majors=[{"major_name": "Ingenieria informática"}, {"major_name":"ingeniería electrónica"}]
    print("majors? ",majors)
    return render_template("admin/adminMajor/majorMenu.html", majors=majors)

@app.route("/admin/major-create")
def admin_major_create():
    return render_template("admin/adminMajor/majorCreate.html")

@app.route("/admin/major-edit")
def admin_major_edit():
    return render_template("admin/adminMajor/majorEdit.html")

@app.route("/admin/major-") #implement major by id
def admin_major():
    return render_template("admin/adminMajor/major.html")

#PROFESSOR ROUTES
@app.route("/professor")
def professor():
    return redirect(url_for("professor_dashboard"))

@app.route("/professor/menu")
def professor_dashboard():
    return render_template("professor/professorDashboard.html")

@app.route("/professor/profile")
def professor_profile():
    return render_template("professor/professorProfileEdit.html")


#STUDENT ROUTES
@app.route("/student")
def student():
    return redirect(url_for("student_dashboard"))

@app.route("/student/menu")
def student_dashboard():
    return render_template("student/studentDashboard.html")

@app.route("/student/profile")
def student_profile():
    return render_template("student/studentProfileEdit.html")




#TEST ROUTE

@app.route("/test")
def test():
    return render_template("/admin/adminMajor/majorMenu.html")