from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def route():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("loginOptions.html")

@app.route("/login/admin")
def login_admin():
    return render_template("loginAdmin.html")

@app.route("/login/student")
def login_student():
    return render_template("loginStudent.html")

@app.route("/login/professor")
def login_professor():
    return render_template("loginProfessor.html")

@app.route("/admin")
def admin():
    return redirect(url_for("admin_menu"))

@app.route("/admin/menu")
def admin_menu():
    return render_template("adminMenu.html")