from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.secret_key = 'sakoblexeyible';

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'noor'
app.config['MYSQL_PASSWORD'] = 'noor123'
app.config['MYSQL_DB'] = 'conference'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM rewievers")
        rewievers = curl.fetchall()
        curl.close()
        print(rewievers)
        return render_template("home.html", data=rewievers)
    else:
        print("alalalal")
        return render_template("home.html")