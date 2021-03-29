from flask import Flask, render_template,flash, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.secret_key = 'sakoblexeyible'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'noor'#'noor''noor''noor'#'aydan'
app.config['MYSQL_PASSWORD'] ='noor123'# 'a1w2k3i4m5..'# 'noor123' 'noor123' 'noor123' 
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

        curl.execute("SELECT * FROM chief_editor")
        chief_editor=curl.fetchall()
        chief_editor = True if len(chief_editor) > 0 else False
                        
        curl.close()

        return render_template("home.html", data=rewievers, authors=authors,papers=papers,chief_editor=chief_editor)
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
    else:
        return render_template("home.html")


@app.route('/rewievers',methods=["GET", "POST"])
def reviewers():
    if request.method == 'POST':

        username = request.form['username']
        firstname = request.form['firstname']
        lastname=request.form['lastname']
        interests = request.form['interests']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rewievers (username, firstname, lastname,interests, email, password) VALUES (%s,%s,%s,%s,%s,%s)",(username, firstname,lastname,interests, email, hash_password))
        mysql.connection.commit()
        return render_template("home.html")
    else:
        print("lalal")
        return render_template("home.html")

@app.route('/chief_editor',methods=["GET", "POST"])
def chief_editor():
    if request.method == 'POST':

        firstname = request.form['firstname']
        lastname=request.form['lastname']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO chief_editor (firstname, lastname, email, password) VALUES (%s,%s,%s,%s)",(firstname,lastname, email, hash_password))
        mysql.connection.commit()
        return render_template("home.html")
    else:
        print("lalal")
        return render_template("home.html")




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
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        country = request.form['country']
        city = request.form['city']
        zip = request.form['zipcode']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO authors (firstname,lastname, phone, email, country, city,zipcode, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(firstname,lastname, phone, email, country, city,zip, hash_password))
        mysql.connection.commit()
        session['name'] = request.form['firstname']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')


        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM admins WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                # return render_template("home.html")
                return redirect(url_for('home'))
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")

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
                session['name'] = user['firstname']
                session['email'] = user['email']
                session['id'] = user['id']
                session['lastname'] = user['lastname']

                print("Session --->>>", session)

                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                user_id = session['id']
                curl.execute("SELECT * FROM papers WHERE user_id=%s",(user_id,))
                papers = curl.fetchall()
                print("Papers ---->", papers)

                return render_template("author.html", name=user['firstname'], papers=papers)
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

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM rewievers WHERE email=%s",(email,))
        user = curl.fetchone()
        
        curl.close()
        print("beafore if ---> ", session)
        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                print("after if ---> ", session)
                session['name'] = user['firstname']
                session['lastname'] = user['lastname']
                session['email'] = user['email']


                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                curl.execute("SELECT * FROM papers")
                papers = curl.fetchall()
                # print("Papers ---->", papers)

                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                curl.execute("SELECT * FROM authors")
                authors = curl.fetchall()



                # print("Authors ---->", authors)

                
                return render_template("reviewers.html", firstname=user['lastname'], papers=papers, authors=authors)
                # return redirect(url_for('login_reviewer', firstname=user['lastname'], papers=papers, authors=authors) )
            else:
                return "Error password and email not match"
        else:
            return "Error Author not found"
    else:
        print("else login if ---> ", session)
        return render_template("login.html")





@app.route('/submit_paper', methods=["GET", "POST"])
def submit_paper(): ##database name is papers
    if request.method == 'GET':
        return render_template("author.html")
    else:
        title = request.form['title']
        interests = request.form['interests']
        keyword = request.form['keyword']
        abstract = request.form['abstract']
        body = request.form['body']

        user_id = session['id']
        user_name = session['firstname']
        user_lastname=session['lastname']
    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO papers (title,interests,keyword,abstract, body,user_id, user_name,user_lastname) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(title,interests,keyword,abstract,body,user_id, user_name,user_lastname))
        mysql.connection.commit()
        return redirect(url_for('submit_paper'))




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
    lastname = request.form['lastname']
    interests = request.form['interests']
    email = request.form['email']

    print("------->>>>>>>",username, firstname, lastname, interests, email)
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # curl.execute("SELECT * from rewievers WHERE id=%s",(id,))

    sql = ("UPDATE rewievers SET username = %s, firstname=%s, lastname=%s, interests=%s, email=%s WHERE id = %s")
    val = (username, firstname, lastname, interests, email, id)
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
