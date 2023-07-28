from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import re
from lib.check_user import check_user

login_bp = Blueprint("login", __name__, url_prefix="/login")

#LOGIN ROUTES
@login_bp.route("/")
def login():
    user_check = check_user(session)

    if(user_check == "student"):
        return redirect(url_for("student.student"))
    elif(user_check == "professor"):
        return redirect(url_for("professor.professor"))
    elif(user_check == "admin"):
        return redirect(url_for("admin.admin"))
    else:
        return render_template("/auth/loginOptions.html")
         
@login_bp.route("/logout")
def logout():
     session.pop("loggedin", None)
     session.pop("nombre", None)
     session.pop("apellido", None)
     session.pop("email", None)
     session.pop("cedula", None)
     return redirect(url_for("login.login"))

@login_bp.route("/admin", methods=["GET","POST"])
def login_admin():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    log_msg = ''
    user_check = check_user(session)
    if(user_check == "student"):
        return redirect(url_for("student.student"))
    elif(user_check == "professor"):
        return redirect(url_for("professor.professor"))
    elif(user_check == "admin"):
        return redirect(url_for("admin.admin"))
    else:
        if request.method == "GET":
            return render_template("/auth/loginAdmin.html")
        if request.method == "POST":
            email = request.form['username'] # Yeah, kinda tricky at first
            password = request.form['password']
            hashed_password = hashlib.sha1((password + current_app.secret_key).encode()).hexdigest()

            cursor.execute("SELECT cedula, nombre, apellido, email FROM admin where email = %s AND password = %s", (email, hashed_password,))
            account = cursor.fetchone()

            if account: 
                session["loggedin"] = True
                session["cedula"] = account["cedula"]
                session["nombre"] = account["nombre"]
                session["apellido"] = account["apellido"]
                session["email"] = account["email"]
                return redirect(url_for("admin.admin"))
            else:
                log_msg = "Email o contraseña incorrectas"
    return render_template("/auth/loginAdmin.html", msg = log_msg)


@login_bp.route("/student", methods = ['GET', 'POST'])
def login_student():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    log_msg = ''
    user_check = check_user(session)
    if(user_check == "student"):
        return redirect(url_for("student.student"))
    elif(user_check == "professor"):
        return redirect(url_for("professor.professor"))
    elif(user_check == "admin"):
        return redirect(url_for("admin.admin"))
    else:
        if request.method == "GET":
            return render_template("/auth/loginStudent.html")
        if request.method == "POST":
            email = request.form['username'] # Yeah, kinda tricky at first
            password = request.form['password']
            hashed_password = hashlib.sha1((password + current_app.secret_key).encode()).hexdigest()
            cursor.execute("SELECT cedula, nombre, apellido, email FROM estudiante where email = %s AND password = %s", (email, hashed_password,))
            account = cursor.fetchone()

            if account: 
                session["loggedin"] = True
                session["cedula"] = account["cedula"]
                session["nombre"] = account["nombre"]
                session["apellido"] = account["apellido"]
                session["email"] = account["email"]
                return redirect(url_for("student.student"))
            else:
                log_msg = "Email o contraseña incorrectas"
    return render_template("/auth/loginStudent.html", msg = log_msg)
    

@login_bp.route("/professor", methods = ['GET', 'POST'])
def login_professor():
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    log_msg = ''
    user_check = check_user(session)
    if(user_check == "student"):
        return redirect(url_for("student.student"))
    elif(user_check == "professor"):
        return redirect(url_for("professor.professor"))
    elif(user_check == "admin"):
        return redirect(url_for("admin.admin"))
    else:
        if request.method == "GET":
            return render_template("/auth/loginProfessor.html")
        if request.method == "POST":
            email = request.form['username'] # Yeah, kinda tricky at first
            password = request.form['password']
            hashed_password = hashlib.sha1((password + current_app.secret_key).encode()).hexdigest()
            cursor.execute("SELECT cedula, nombre, apellido, email FROM profesor where email = %s AND password = %s", (email, hashed_password,))
            account = cursor.fetchone()

            if account: 
                session["loggedin"] = True
                session["cedula"] = account["cedula"]
                session["nombre"] = account["nombre"]
                session["apellido"] = account["apellido"]
                session["email"] = account["email"]
                return redirect(url_for("professor.professor"))
            else:
                log_msg = "Email o contraseña incorrectas"
    return render_template("/auth/loginProfessor.html", msg = log_msg)
    
