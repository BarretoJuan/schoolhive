from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def route():
    return render_template("adminMenu.html")

@app.route("/login")
def hello_world():
    return render_template("adminMenu.html")

@app.route("/login/admin")
def login_admin():
    return render_template("loginAdmin.html")

@app.route("/login/student")
def login_student():
    return render_template("loginStudent.html")

@app.route("/login/professor")
def login_professor():
    return render_template("loginProfessor.html")