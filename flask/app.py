from sre_constants import SUCCESS
from flask import Flask, render_template, request, flash, redirect
from flask import *
import os
import shutil
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import mysql
import json
import subprocess
import urllib.request
import MySQLdb.cursors
import sys
from flask_mysqldb import MySQL
import mysql.connector
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
CORS(app, support_credentials=True)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Pass'
# app.config['MYSQL_DB'] = 'db name'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)

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
                f=open(os.path.join(root, file),'rb')
                f.close()
                return_Dict.append(f.name)
    return return_Dict

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

#Index
@app.route('/index')
def index():
    context = { 'server_time': format_server_time() }
    return render_template('index_old.html', context=context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
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
        if data is not None:
            session['logged_in'] = True
            return "Sucess"
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@app.route('/api', methods=["POST", "GET"])
def page2():
    return SUCCESS


# @app.route("/api2", methods=['POST', 'GET'])
# def page3():
#     cur = mysql.connection.cursor()
#     #cursor = mysql.connection.cursor()
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     verify = cur.execute(
#     "Select password from login WHERE emailid= %s ", (,))
#     if verify > 0:
#         row = cur.fetchall()
#         for dict in row:
#             #do here
#     return render_template()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404

port = int(os.environ.get('PORT', 8080))
if __name__ == "__main__":
    app.run(debug=True)
