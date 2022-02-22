from flask import Flask, render_template, request, flash, redirect
from flask import *
import os
import shutil
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
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cairocoders-ednalan'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pass'
app.config['MYSQL_DB'] = 'db name'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/', methods=["POST", "GET"])
def hello():
    return render_template('Homepage.html')


@app.route('/page2', methods=["POST", "GET"])
def page2():
    return render_template('page2.html')


@app.route("/page3", methods=['POST', 'GET'])
def page3():
    cur = mysql.connection.cursor()
    #cursor = mysql.connection.cursor()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        print("hello")
    return render_template('page3.html')


if __name__ == "__main__":
    app.run(debug=True)
