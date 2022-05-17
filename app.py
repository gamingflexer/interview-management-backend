from app import app
import time
from werkzeug.utils import secure_filename
import pymysql
pymysql.install_as_MySQLdb()
from flask_cors import CORS, cross_origin
import mysql.connector
from flask_mysqldb import MySQL
import sys
import MySQLdb.cursors
import urllib.request
import subprocess
import json
import mysql
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL, MySQLdb
from sre_constants import SUCCESS
from flask import Flask, render_template, request, flash, redirect
from flask import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
CORS(app, support_credentials=True)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

app.config['MYSQL_HOST'] = 'dpomserver.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'dpomserver@dpomserver'
app.config['MYSQL_PASSWORD'] = '#Freelance#123'
app.config['MYSQL_DB'] = 'miniproject'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def format_server_time():
    server_time = time.localtime()
    return time.strftime("%I:%M:%S %p", server_time)


def getFileContent(path_dir):
    return_Dict = []
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            if root in path_dir:
                f = open(os.path.join(root, file), 'rb')
                f.close()
                return_Dict.append(f.name)
    return return_Dict

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# Index


@app.route('/index')
def index():
    context = {'server_time': format_server_time()}
    return render_template('index_old.html', context=context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(
                User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if u == "admin@gmail.com" and p == "admin":
            return redirect("http://localhost:3000/", code=200)
        elif data is not None:
            session['logged_in'] = True
            return render_template('exam_form.html', message="Incorrect Details")
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@app.route('/seec', methods=["POST", "GET"])
def showall():
    cur = mysql.connection.cursor()
    data = cur.execute(
        "Select * from candidates ")
    if data > 0:
        row = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return {"data":row}


@app.route('/addc=<string:name>=<int:number>=<string:email>=<int:age>=<string:qualify>', methods=["POST", "GET"])
def addc(name,number,email,age,qualify):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO candidates(name,contact,email,age,qualify) VALUES (%s,%s,%s,%s,%s)", (name,number,email,age,qualify,))
    mysql.connection.commit()
    cur.close()
    return "Candidate added"


@app.route('/deletec=<int:id>', methods=["POST", "GET"])
def deletec(id):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM candidates WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return "Candidates Deleted"

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

@app.route('/seeq', methods=["POST", "GET"])
def seeq():
    cur = mysql.connection.cursor()
    data = cur.execute(
        "Select * from questions")
    if data > 0:
        row = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return {"data":row}


@app.route('/addq=<string:question>=<string:grades>', methods=["POST", "GET"])
def addq(question, grades):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO questions(questions,answers) VALUES (%s, %s)", (question, grades,))
    mysql.connection.commit()
    cur.close()
    return "Question Added"


@app.route('/deleteq=<int:qid>', methods=["POST", "GET"])
def deleteq(qid):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM questions WHERE qid=%s", (qid,))
    mysql.connection.commit()
    cur.close()
    return "Question Deleted"


@app.route('/seem=<int:qid>', methods=["POST", "GET"])
def seem(qid):
    cur = mysql.connection.cursor()
    data = cur.execute(
        "Select * from candidates WHERE qid=%s", (qid,))
    if data > 0:
        row = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return {"data":row}


@app.route('/addmarks=<int:marks>=<int:id>', methods=["POST", "GET"])
def marksadd(marks,id):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE candidates SET marks=%s WHERE id=%s", (marks,id,))
    mysql.connection.commit()
    cur.close()
    return "marks added"

@app.route('/form-fill', methods=["POST", "GET"])
def exam():
    return render_template('exam_form.html')


@app.route('/submitted', methods=["POST", "GET"])
def booked():
    name = request.form.get('name')
    id = request.form.get('id')
    q1 = request.form.get('q1')
    q2 = request.form.get('q2')
    q3 = request.form.get('q3')
    q4 = request.form.get('q4')
    q5 = request.form.get('time_slot')
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO candidates(name,email,edu,ach,pro,exp,nexp) VALUES (%s,%s,%s,%s,%s,%s,%s)", (id,name,q1,q2,q3,q4,q5,))
    mysql.connection.commit()
    cur.close()
    return render_template('submitted.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404


port = int(os.environ.get('PORT', 8080))
if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
