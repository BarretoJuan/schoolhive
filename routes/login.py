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
         
    # if "loggedin " in session:
    #         mysql = current_app.config['MYSQL']
    #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    #         check_student = '''
    #         SELECT CEDULA FROM estudiante WHERE CEDULA = %s
    #     '''
    #         check_admin = '''
    #         SELECT CEDULA FROM admin WHERE CEDULA = %s
    #     '''
    #         check_professor = '''
    #         SELECT CEDULA FROM profesor WaHERE CEDULA = %s
    #     '''
    #         cursor.execute(check_student, (session['cedula'],))
    #         student=cursor.fetchone()

    #         cursor.execute(check_admin, (session['cedula'],))
    #         admin=cursor.fetchone()

    #         cursor.execute(check_professor, (session['cedula'],))
    #         professor=cursor.fetchone()

    #         if student:
    #               return redirect(url_for("student.student"))
    #         elif admin:
    #               return redirect(url_for("admin.admin"))
    #         elif professor:
    #               return redirect(url_for("professor.professor"))
    #         else:
    #               return "notLoggedIn"
    
    # else:
    #         return render_template("/auth/loginOptions.html")
        
  


@login_bp.route("/admin")
def login_admin():
    return render_template("/auth/loginAdmin.html")

@login_bp.route("/student")
def login_student():
    return render_template("/auth/loginStudent.html")

@login_bp.route("/professor")
def login_professor():
    return render_template("/auth/loginProfessor.html")

