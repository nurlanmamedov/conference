from flask import Flask, render_template,flash, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.secret_key = 'sakoblexeyible'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'aydan' ##'noor'
app.config['MYSQL_PASSWORD'] ='a1w2k3i4m5..'##'noor123' #'
app.config['MYSQL_DB'] = 'conference'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM rewievers")
        rewievers = curl.fetchall()
        print("All rewievers --> ", rewievers)
        curl.execute("SELECT * FROM authors")
        authors = curl.fetchall()
        curl.execute("SELECT * FROM papers")
        papers=curl.fetchall()
        curl.close()

        return render_template("home.html", data=rewievers, authors=authors,papers=papers)
    else:
        print("alalalal")
        return render_template("home.html")


@app.route('/authors',methods=["GET", "POST"])
def authors():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors")
        authors = curl.fetchall()
        curl.close()
        print(authors)
        return render_template("home.html", authors=authors)

    # if request.method == 'POST':

    #     username = request.form['username']
    #     fullname = request.form['fullname']
    #     institution = request.form['institution']
    #     email = request.form['email']
    #     password = request.form['password'].encode('utf-8')
    #     hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

    #     cur = mysql.connection.cursor()
    #     cur.execute("INSERT INTO rewievers (username, fullname, institution, email, password) VALUES (%s,%s,%s,%s,%s)",(username, fullname, institution, email, hash_password))
    #     mysql.connection.commit()
    #     return render_template("home.html")
    else:
        return render_template("home.html")


@app.route('/rewievers',methods=["GET", "POST"])
def reviewers():
    if request.method == 'POST':

        username = request.form['username']
        firstname = request.form['firstname']
        surname=request.form['surname']
        interests = request.form['interests']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rewievers (username, firstname, surname,interests, email, password) VALUES (%s,%s,%s,%s,%s,%s)",(username, firstname,surname,interests, email, hash_password))
        mysql.connection.commit()
        return render_template("home.html")
    else:
        print("lalal")
        return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')


        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():

    session.clear()
    flash("You successfully logged out")
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("author_registration.html")
    else:
        name = request.form['name']
        surname = request.form['surname']
        interests = request.form['interests']
        phone = request.form['phone']
        email = request.form['email']
        country = request.form['country']
        city = request.form['city']
        zip = request.form['zipcode']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO authors (name,surname,interests, phone, email, country, city,zipcode, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,surname,interests, phone, email, country, city,zip, hash_password))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))


@app.route('/login_author', methods=["GET", "POST"])
def login_author():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        print("email --> ",password)
        print("password --> ",password)

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors WHERE email=%s",(email,))
        user = curl.fetchone()
        print("User --> ",user)
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("author.html", name=user['name'])
            else:
                return "Error password and email not match"
        else:
            return "Error Author not found"
    else:
        return render_template("login.html")


@app.route('/login_reviewer', methods=["GET", "POST"])
def login_reviewer():
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password'].encode('utf-8')

        print("email --> ",password)
        print("password --> ",password)

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM rewievers WHERE email=%s",(email,))
        user = curl.fetchone()
        print("User --> ",user)
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['firstname'] = user['firstname']
                session['surname'] = user['surname']

                session['email'] = user['email']

                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                curl.execute("SELECT * FROM papers")
                papers = curl.fetchall()
                print("Papers ---->", papers)
                return render_template("reviewers.html", name=user['username'], papers=papers)
            else:
                return "Error password and email not match"
        else:
            return "Error Author not found"
    else: 
        return render_template("login.html")





@app.route('/submit_paper', methods=["GET", "POST"])
def submit_paper(): ##database name is papers
    if request.method == 'GET':
        return render_template("author.html")
    else:
        title = request.form['title']
        topic = request.form['topic']
        keyword = request.form['keyword']
        abstract = request.form['abstract']
        body = request.form['body']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO papers (title,topic,keyword,abstract, body) VALUES (%s,%s,%s,%s,%s)",(title,topic,keyword,abstract,body))
        mysql.connection.commit()
        session['title'] = request.form['title']
        session['keyword'] = request.form['keyword']
        return redirect(url_for('home'))




@app.route('/papers',methods=["GET", "POST"])
def papers():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM papers")
        papers = curl.fetchall()
        curl.close()
        print(papers)
        return render_template("login.html", papers=papers)


@app.route('/papers1',methods=["GET", "POST"])
def get_papers():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM papers")
        papers = curl.fetchall()
        curl.close()
        return papers
        # print("papers 11111 --->>", papers1)
        # return render_template("reviewers.html", papers1=papers1)




@app.route('/delete_rewiever/<id>/',methods=["GET", "POST"])
def delete_rewiever(id):
        print("Delete id --> ", id)
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("DELETE from rewievers WHERE id=%s",(id,))
        curl.close()
        mysql.connection.commit()
        return redirect(url_for('home'))


@app.route('/update_rewiever/<int:id>/', methods = ['GET', 'POST'])
def update_rewiever(id):
    username = request.form['username']
    firstname = request.form['firstname']
    surname = request.form['surname']
    interests = request.form['interests']
    email = request.form['email']

    print("------->>>>>>>",username, firstname, surname, interests, email)
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # curl.execute("SELECT * from rewievers WHERE id=%s",(id,))

    sql = ("UPDATE rewievers SET username = %s, firstname=%s, surname=%s, interests=%s, email=%s WHERE id = %s")
    val = (username, firstname, surname, interests, email, id)
    curl.execute(sql, val)
    curl.close()
    mysql.connection.commit()
 
    return redirect(url_for('home'))





@app.route('/direct', methods=["GET"])
def direct_pages(): ##database name is papers
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors")
        authors = curl.fetchall()
        curl.close()
        return render_template("view.html", authors=authors)



if __name__ == '__main__':
    app.debug = True
    app.run()
