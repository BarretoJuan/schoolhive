import MySQLdb
from flask import current_app, session
from flask_mysqldb import MySQL

def check_user (session):
    if "loggedin" in session:
            mysql = current_app.config['MYSQL']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            check_student = '''
            SELECT CEDULA FROM estudiante WHERE CEDULA = %s
            '''
            check_admin = '''
            SELECT CEDULA FROM admin WHERE CEDULA = %s
            '''
            check_professor = '''
            SELECT CEDULA FROM profesor WHERE CEDULA = %s
            '''
            cursor.execute(check_student, (session['cedula'],))
            student=cursor.fetchone()

            cursor.execute(check_admin, (session['cedula'],))
            admin=cursor.fetchone()

            cursor.execute(check_professor, (session['cedula'],))
            professor=cursor.fetchone()

            if student:
                  return "student"
            elif admin:
                  return "admin"
            elif professor:
                  return "professor"
            else:
                  return "notLoggedIn"
    else:
        return "notLoggedIn"
        




