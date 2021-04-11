from flask import Flask, render_template,flash, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)
app.secret_key = 'sakoblexeyible'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'noor'#'noor'#'noor''noor''noor'#'aydan'
app.config['MYSQL_PASSWORD'] ='noor123'#'noor123'# # 'noor123' 'noor123' 'noor123' 
app.config['MYSQL_DB'] = 'conference'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM reviewers1")
        rewievers = curl.fetchall()
        print("All rewievers --> ", rewievers)
        curl.execute("SELECT * FROM authors1 ")
        authors = curl.fetchall()
        curl.execute("SELECT * FROM papers1 ")
        papers=curl.fetchall()

        curl.execute("SELECT * FROM interests1")
        interests=curl.fetchall()

        print("interests list --> ", interests)

        curl.execute("SELECT * FROM chief_editor")
        chief_editor=curl.fetchall()
        chief_editor = True if len(chief_editor) > 0 else False
                        
        curl.close()

        return render_template("home.html", data=rewievers, authors=authors,papers=papers,chief_editor=chief_editor, interests=interests)
    else:
        print("alalalal")
        return render_template("home.html")


@app.route('/authors',methods=["GET", "POST"])
def authors():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors1")
        authors = curl.fetchall()
        curl.close()
        print(authors)
        return render_template("home.html", authors=authors)
    else:
        return render_template("home.html")


@app.route('/rewievers',methods=["GET", "POST"])
def reviewers():
    if request.method == 'POST':

        firstname = request.form['firstname']
        lastname=request.form['lastname']
        email = request.form['email']
        interest_id = int(request.form['interest_id'])
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviewers1 (firstname, lastname, interest_id, email, password) VALUES (%s,%s,%s,%s,%s)",( firstname,lastname,interest_id,email, hash_password))
        mysql.connection.commit()
        return render_template("home.html")
    else:

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
        cur.execute("INSERT INTO authors1 (firstname,lastname, phone, email, country, city,zipcode, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(firstname,lastname, phone, email, country, city,zip, hash_password))
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
        curl.execute("SELECT * FROM authors1 WHERE email=%s",(email,))
        user = curl.fetchone()
        print("User --> ",user)
        curl.close()
        
        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['firstname']
                session['email'] = user['email']
                session['id'] = user['author_id']
                session['lastname'] = user['lastname']

                print("Session --->>>", session)

                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                author_id = session['id']
                
                # curl.execute("SELECT * FROM papers1 WHERE author_id=%s",(author_id,))
                curl.execute("SELECT * FROM papers1 LEFT JOIN interests1 using(interest_id) WHERE author_id=%s",(author_id,))

                papers = curl.fetchall()

                curl.execute("SELECT * FROM interests1")

                interests = curl.fetchall()
                print("Papers for nurlan ---->", papers)

                return render_template("author.html", name=user['firstname'], papers=papers, interests=interests)
            else:
                return "Error password and email not match"
        else:
            return "Error Author not found"
    else:
        return render_template("login.html")


@app.route('/rating', methods=["GET", "POST"])
def rating():
    # rate = request.form["star"]
    if request.method == 'POST':
        rate = request.form["star"]
        print("rating --> ", rate)
        # return redirect(url_for('login_reviewer'))
        return render_template("reviewers.html")



@app.route('/login_reviewer', methods=["GET", "POST"])
def login_reviewer():
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM reviewers1 WHERE email=%s",(email,))
        
        
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
                curl.execute("SELECT * FROM papers1")
                papers = curl.fetchall()
                # print("Papers ---->", papers)

                curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                curl.execute("SELECT * FROM authors1")
                curl.execute("SELECT * FROM papers1")
                authors = curl.fetchall()

                curl.execute("SELECT Distinct papers1.paper_id, authors1.firstname,authors1.lastname, papers1.title, papers1.body, interests1.interest_name FROM papers1 INNER JOIN authors1 INNER JOIN reviewers1 INNER JOIN interests1 ON (papers1.author_id = authors1.author_id AND papers1.interest_id = 4 AND reviewers1.reviewer_id=1 AND interests1.interest_id=4)")
                answer = curl.fetchall()
                print("answer ----++++++++++++_________++++++++++++++++++----------------+++++++++++++++++++", answer)

                
                return render_template("reviewers.html", firstname=user['lastname'], papers=papers, authors=authors, answer=answer)
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
        interest_id = request.form['interest_id']
        author_id = session['id']
        keywords = request.form['keywords']
        abstract = request.form['abstract']
        body = request.form['body']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO papers1 (title, interest_id, author_id, keywords, abstract, body) VALUES (%s,%s,%s,%s,%s,%s)",(title,interest_id,author_id,keywords,abstract,body, ))
        mysql.connection.commit()
        return redirect(url_for('submit_paper'))




@app.route('/papers',methods=["GET", "POST"])
def papers():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM papers1 ")
        papers = curl.fetchall()
        curl.close()
        print(papers)
        return render_template("login.html", papers=papers)


@app.route('/papers1',methods=["GET", "POST"])
def get_papers():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM papers1 ")
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

    firstname = request.form['firstname']
    lastname = request.form['lastname']
   
    email = request.form['email']

    print("------->>>>>>>",firstname, lastname, email)
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # curl.execute("SELECT * from rewievers WHERE id=%s",(id,))

    sql = ("UPDATE rewievers SET firstname=%s, lastname=%s, email=%s WHERE id = %s")
    val = ( firstname, lastname, email, id)
    curl.execute(sql, val)
    curl.close()
    mysql.connection.commit()
 
    return redirect(url_for('home'))





@app.route('/direct', methods=["GET"])
def direct_pages(): ##database name is papers
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors1 ")
        authors = curl.fetchall()
        curl.close()
        return render_template("view.html", authors=authors)



if __name__ == '__main__':
    app.debug = True
    app.run()
