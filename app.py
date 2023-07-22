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