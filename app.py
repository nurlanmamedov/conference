from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import json
from flask_session import Session





app = Flask(__name__)
app.secret_key = "sakoblexeyible"
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "aydan"  # 'noor'#'aydan'
app.config["MYSQL_PASSWORD"] = "a1w2k3i4m5.."  # "a1w2k3i4m5.."'noor123'
app.config["MYSQL_DB"] = "conference"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def home():
    print("here is our sesion *******/*/*/*/*4/45454/54/54/54",session)

    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM reviewers1")
        rewievers = curl.fetchall()

        curl.execute("SELECT * FROM authors1 ")
        authors = curl.fetchall()

        curl.execute(
            "SELECT Distinct firstname, lastname,  final_status.*  from conference.final_status  INNER JOIN authors1 ON (authors1.author_id = final_status.author_id ) WHERE evaluate is not null"
        )
        papers = curl.fetchall()

        curl.execute("SELECT * FROM papers1 ")
        papers1 = curl.fetchall()
        papers_result = {}
        for i in papers1:
            papers_result[i["paper_id"]] = i

        curl.execute("SELECT * FROM interests1")
        interests = curl.fetchall()

        curl.execute("SELECT * FROM chief_editor")
        chief_editor = curl.fetchall()
        chief_editor = True if len(chief_editor) > 0 else False
        curl.close()

        return render_template(
            "home.html",
            data=rewievers,
            authors=authors,
            papers=papers,
            chief_editor=chief_editor,
            interests=interests,
            papers1=papers1,
            papers_result=papers_result,
        )
    else:
        return render_template("home.html")


@app.route("/authors", methods=["GET", "POST"])
def authors():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors1")
        authors = curl.fetchall()
        curl.close()
        return render_template("home.html", authors=authors)
    else:
        return render_template("home.html")


@app.route("/rewievers", methods=["GET", "POST"])
def reviewers():
    if request.method == "POST":

        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        interest_id = int(request.form["interest_id"])
        password = request.form["password"].encode("utf-8")
        password2 = request.form["password2"].encode("utf-8")

        if not firstname or not lastname or not email or not password or not password2:
            flash("You can not leave this place empty,Please fill out!!")
            return redirect('/')
        elif "@" not in email:
            flash("You must include '@' into email")
            print("huhuhu")
            return redirect('/')
        elif password != password2:
            flash("Passwords dont match!!")
            return redirect('/')
        elif not len(password)>=8:
            flash('You must write at least 8 charachters in length')
            print("huhuhu")
            return redirect('/')

        curl = mysql.connection.cursor()
        curl.execute(
            "SELECT count(*) FROM conference.reviewers1 where interest_id=%s",
            (interest_id,),
        )
        count = curl.fetchall()
        count = count[0]["count(*)"]
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        if int(count) < 3:
            curl.execute(
                "INSERT INTO reviewers1 (firstname, lastname, interest_id, email, password) VALUES (%s,%s,%s,%s,%s)",
                (firstname, lastname, interest_id, email, hash_password),
            )
            mysql.connection.commit()
            flash('Congratulations! You have sucessfully added a reviewer.')
            return redirect("/")
        else:
            message = "Sorry, but limit of interests is exceed"
            backUrl = "/"
            return render_template(
                "reviewer_exceed.html", message=message, backUrl=backUrl
            )
    else:

        return render_template("home.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have successfully logged out")
    return redirect("login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("author_registration.html")
    else:
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phone = request.form["phone"]
        email = request.form["email"]
        country = request.form["country"]
        city = request.form["city"]
        zip = request.form["zipcode"]
        password = request.form['password'].encode('utf-8')
        hash_password1 = bcrypt.hashpw(password, bcrypt.gensalt())       
        password2 = request.form['password2'].encode('utf-8')
        hash_password2 = bcrypt.hashpw(password2, bcrypt.gensalt())
        
        if not firstname or not lastname or not phone or not email or not country or not city or not zip or not password or not password2:
            flash("You can not leave this place empty,Please fill out!!")
            return redirect('register')
        elif "@" not in email:
            flash("You must include '@' into email")
            print("huhuhu")
            return redirect('register')
        elif password != password2:
            flash("Passwords dont match!!")
            return redirect('register')
        elif not len(password)>=8:
            flash('You must write at least 8 charachters in length')
            print("huhuhu")
            return redirect('register')
        elif not phone.isnumeric():
            flash('Include a correct phone number')
            print("huhuhu")
            return redirect('register')
            
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO authors1 (firstname,lastname, phone, email, country, city,zipcode, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (firstname, lastname, phone, email, country, city, zip, hash_password),
        )
        
        mysql.connection.commit()
        email=request.form['email']
        return render_template("login_success.html",email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM admins WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()
        try:
            if len(user) > 0:
                if bcrypt.hashpw(password, user["password"].encode("utf-8")) == user[
                    "password"
                ].encode("utf-8"):
                    session["name"] = user["name"]
                    session["email"] = user["email"]
                    return redirect(url_for("home"))
                else:
                    return render_template("error.html")
        except:
            return render_template("notfound.html")
    else:
        return render_template("login.html")


@app.route("/login_author", methods=["GET", "POST"])
def login_author():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")

        print("email --> ", password)
        print("password --> ", password)

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors1 WHERE email=%s", (email,))
        user = curl.fetchone()
        print("User --> ", user)
        curl.close()
        try:
            if len(user) > 0:
                if bcrypt.hashpw(password, user["password"].encode("utf-8")) == user[
                    "password"
                ].encode("utf-8"):
                    session["email"] = user["email"]
                    session["author_id"] = user["author_id"]
                    session["name"] = user["firstname"]
                    session["lastname"] = user["lastname"]

                    print("Session --->>>", session)

                    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    author_id = session["author_id"]

                    curl.execute(
                        "SELECT * FROM papers1 LEFT JOIN interests1 using(interest_id) WHERE author_id=%s",
                        (author_id,),
                    )

                    papers = curl.fetchall()
                    curl.execute("SELECT * FROM interests1")
                    interests = curl.fetchall()
                    data = {
                        "name": user["firstname"],
                        "lastname": user["lastname"],
                        "papers": papers,
                        "interests": interests,
                    }
                    session["author_data"] = data
                    return redirect(url_for("author_page"))
                else:
                    return render_template("error.html")
        except:
            return render_template("notfound.html")
    else:
        return render_template("login.html")


@app.route("/author_page", methods=["GET", "POST"])
def author_page():
    if request.args.get("title"):
        title = request.args.get("title")
        body = request.args.get("body")
        keywords = request.args.get("keywords")
        abstract = request.args.get("abstract")
        paper_id = request.args.get("paperID")
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "UPDATE papers1 SET title=%s, keywords=%s, body=%s, abstract=%s WHERE paper_id = %s"
        val = (title, keywords, body, abstract, paper_id)
        curl.execute(sql, val)
        # curl.close()
        mysql.connection.commit()
        flash("The paper has been updated")
        return redirect(url_for("author_page"))

    if session.get("author_id") != None:
        if session["author_data"]:
            name = session["author_data"]["name"]
            lastname = session["author_data"]["lastname"]
            interests = session["author_data"]["interests"]
        curl = mysql.connection.cursor()
        curl.execute(
            "SELECT * FROM papers1 LEFT JOIN interests1 using(interest_id) WHERE author_id=%s",
            (session.get("author_id"),),
        )
        papers = curl.fetchall()
        session["author_data"]["papers"] = papers

        curl.execute("SELECT * FROM final_status")
        final_status = curl.fetchall()

        rate_list = {}
        for i in final_status:
            curl.execute(
                "SELECT Distinct final_status.paper_id, final_status.author_id, final_status.evaluate, group_concat(paper_status1.comment) as comments  FROM final_status INNER JOIN paper_status1  ON (final_status.paper_id = paper_status1.paper_id AND final_status.paper_id = %s)",
                (i["paper_id"],),
            )
            rate_list[i["paper_id"]] = curl.fetchone()
        return render_template(
            "author.html",
            name=name,
            lastname=lastname,
            papers=papers,
            interests=interests,
            rate_list=rate_list,
        )
    else:
        redirect(url_for("login_author"))


@app.route("/update_papers", methods=["GET", "POST"])
def update_papers():

    try:

        if request.method == "GET":
            return render_template("author.html")
        else:
            title = request.form["title"]
            keywords = request.form["keywords"]
            body = request.form["body"]
            abstract = request.form["abstract"]
            paperID = request.form["paperID"]

            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = "UPDATE papers1 SET title=%s, keywords=%s, body=%s, abstract=%s WHERE paper_id = %s"
            val = (title, keywords, body, abstract, paperID)
            curl.execute(sql, val)
            mysql.connection.commit()
            curl.close()
            flash("The paper has been updated")
            return redirect(url_for("author_page"))
    except MySQLdb.Error as  err:
        curl.close()
        flash("Please do not exeed 100words" )
        return redirect(url_for("author_page"))

@app.route("/rating", methods=["GET", "POST"])
def rating():
    # rate = request.form["star"]
    if request.method == "POST":
        rating = request.form["star"]
        comment = request.form["comment"]
        paper_id = request.form["submit_b"]
        reviewer_id = session["reviewer_id"]
        author_id = request.form["author_id"]

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute(
            "SELECT count(*) as cnt FROM paper_status1 WHERE reviewer_id=%s AND paper_id=%s",
            (reviewer_id, paper_id),
        )
        count = curl.fetchone()
        curl.execute("SELECT * FROM paper_status1")
        status = curl.fetchall()
        if count["cnt"] == 0:
            curl.execute(
                "INSERT INTO paper_status1 (reviewer_id, paper_id,author_id, rating, comment) VALUES (%s,%s,%s,%s,%s)",
                (
                    reviewer_id,
                    paper_id,
                    author_id,
                    rating,
                    comment,
                ),
            )
        else:
            curl.execute(
                "UPDATE paper_status1 SET rating = %s, comment=%s WHERE reviewer_id = %s AND paper_id=%s",
                (
                    rating,
                    comment,
                    reviewer_id,
                    paper_id,
                ),
            )
        mysql.connection.commit()
        result = curl.fetchall()
        return redirect(url_for("reviewer_page"))


@app.route("/login_reviewer", methods=["GET", "POST"])
def login_reviewer():

    if session.get("rewiever_id"):
        return redirect(url_for("reviewer_page"))
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM reviewers1 WHERE email=%s", (email,))
        
        user = curl.fetchone()
        print("user*/*/**/*/*/*/*/*/*/*",session,user)
        curl.close()
        try:
            if len(user) > 0:
                print('usrmizi burdadi>0',user)
                if bcrypt.hashpw(password, user["password"].encode("utf-8")) == user[ "password"].encode("utf-8"):
                    print("after if ---> ", session)
                    print("after if 34rd---> ", session)
                    session["name"] = user["firstname"]
                    session["lastname"] = user["lastname"]
                    session["email"] = user["email"]
                    session["reviewer_id"] = user["reviewer_id"]
                    session["interest_id"] = user["interest_id"]
                    print("after if --->2 ", session)

                    rew_id = session["reviewer_id"]
                    int_id = session["interest_id"]

                    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    curl.execute("SELECT * FROM papers1")
                    papers = curl.fetchall()

                    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    curl.execute("SELECT * FROM authors1")
                    curl.execute("SELECT * FROM papers1")
                    authors = curl.fetchall()

                    curl.execute(
                        "SELECT Distinct papers1.paper_id, papers1.abstract, authors1.firstname,authors1.lastname,authors1.author_id, papers1.title, papers1.body, interests1.interest_name FROM papers1 INNER JOIN authors1 INNER JOIN reviewers1 INNER JOIN interests1 ON (papers1.author_id = authors1.author_id AND papers1.interest_id = %s AND reviewers1.reviewer_id=%s AND interests1.interest_id=%s)",
                        (
                            int_id,
                            rew_id,
                            int_id,
                        ),
                    )
                    answer = curl.fetchall()

                    data = {
                        "firstname": user["lastname"],
                        "papers": papers,
                        "authors": authors,
                        "answer": answer,
                    }
                    session["data"] = data
                    return redirect(url_for("reviewer_page"))
                else:
                    return render_template("error.html")
                    
        except:
            return render_template("notfound.html")
    else:
        print("else login if ---> ", session)
        return render_template("login.html")


@app.route("/reviewer_page", methods=["GET", "POST"])
def reviewer_page():
    if session.get("reviewer_id") != None:
        if session["data"]:
            firstname = session["data"]["firstname"]
            papers = session["data"]["papers"]
            authors = session["data"]["authors"]
            answer = session["data"]["answer"]

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM final_status")
        final_status = cur.fetchall()

        final_status_result = {}
        for i in final_status:
            final_status_result[i["paper_id"]] = i["evaluate"]
        print("||||||||||||||||||", final_status)
        print("||||||||||||||||||", final_status_result)
        return render_template(
            "reviewers.html",
            firstname=firstname,
            papers=papers,
            authors=authors,
            answer=answer,
            final_status=final_status_result,
        )
    else:
        redirect(url_for("login_reviewer"))


@app.route("/submit_paper", methods=["GET", "POST"])
def submit_paper():  # database name is papers
    try:
        if request.method == "GET":
            return render_template("author.html")
        else:
            title = request.form["title"]
            interest_id = request.form["interest_id"]
            author_id = session["author_id"]
            keywords = request.form["keywords"]
            abstract = request.form["abstract"]
            body = request.form["body"]

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO papers1 (title, interest_id, author_id, keywords, abstract, body) VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    title,
                    interest_id,
                    author_id,
                    keywords,
                    abstract,
                    body,
                ),
            )
            mysql.connection.commit()
            return render_template("submit_sucess.html")
    except MySQLdb.Error as  err:
        cur.close()
        flash("No valid data ..." )
        return redirect(url_for("author_page"))



@app.route("/papers", methods=["GET", "POST"])
def papers():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM papers1 ")
        papers = curl.fetchall()
        curl.close()
        print(papers)
        return render_template("login.html", papers=papers)


@app.route("/papers1", methods=["GET", "POST"])
def get_papers():
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM papers1 ")
        papers = curl.fetchall()
        curl.close()
        return papers


@app.route("/delete_rewiever/<id>/", methods=["GET", "POST"])
def delete_rewiever(id):
    print("Delete id --> ", id)
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("DELETE from reviewers1 WHERE reviewer_id=%s", (id,))
    curl.close()
    mysql.connection.commit()
    return redirect(url_for("home"))


@app.route("/update_rewiever/<int:id>/", methods=["GET", "POST"])
def update_rewiever(id):

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    password = request.form["password"].encode("utf-8")

    password = bcrypt.hashpw(password, bcrypt.gensalt())
    email = request.form["email"]

    print("------->>>>>>>", firstname, lastname, email)
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    sql = "UPDATE reviewers1 SET firstname=%s, lastname=%s, email=%s, password=%s WHERE reviewer_id = %s"
    val = (firstname, lastname, email, password, id)
    curl.execute(sql, val)
    curl.close()
    mysql.connection.commit()
    flash("Reviewer has been successfully updated")
    return redirect(url_for("home"))


@app.route("/direct_page", methods=["GET"])
def direct_pages():  # database name is papers
    if request.method == "GET":
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM authors1 ")
        authors = curl.fetchall()

        curl.execute("SELECT * FROM interests1")
        interests = curl.fetchall()
        curl.close()
        flash("Congratulations,Author has been assignes as a reviewer")
        return render_template("view.html", authors=authors, interests=interests)


@app.route("/delete_paper/<id>/", methods=["GET", "POST"])
def delete_paper(id):

    print("Delete paper --> ", id)
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("DELETE from papers1 WHERE paper_id=%s", (id,))
    curl.close()
    mysql.connection.commit()
    flash("Paper has been successfully deleted")
    return redirect(url_for("author_page"))


@app.route("/login_chief_editor", methods=["GET", "POST"])
def login_chief_editor():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")

        print("password --> ", password)
        print("email --> ", email)

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM chief_editor WHERE email=%s", (email,))
        user = curl.fetchone()
        print("User --> ", user)
        curl.close()
        try:
            if len(user) > 0:

                print("password", password)
                print("user password utf encode", user["password"].encode("utf-8"))

                if bcrypt.hashpw(password, user["password"].encode("utf-8")) == user[
                    "password"
                ].encode("utf-8"):
                    session["firstname"] = user["firstname"]
                    session["lastname"] = user["lastname"]
                    session["email"] = user["email"]
                    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    curl.execute(
                        "SELECT sum(rating) as point, GROUP_CONCAT(comment) as comments, firstname, lastname, author_id, paper_id FROM  conference.paper_status1 LEFT JOIN conference.authors1 using(author_id) WHERE author_id=author_id GROUP BY conference.paper_status1.paper_id HAVING count(conference.paper_status1.reviewer_id)=3"
                    )
                    data = curl.fetchall()
                    curl.execute("SELECT * FROM final_status")
                    final_status = curl.fetchall()

                    print("finaaaaaaaaal", final_status)

                    for i in data:
                        i["point"] = int(i["point"])
                    result_status = {}
                    for i in final_status:
                        result_status[i["paper_id"]] = i["evaluate"]

                    session["final_status"] = result_status
                    session["data"] = data

                    return redirect(url_for("chief_editor_page"))
                else:
                    return render_template("error.html")

        except:
            return render_template("notfound.html")
    else:
        return render_template("login.html")


@app.route("/evaluate_accept", methods=["GET", "POST"])
def evaluate_accept():

    evaluate = request.form["evaluate"]
    paper_id = request.form["paper_id"]
    author_id = request.form["author_id"]
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print(curl)
    curl.execute(
        "INSERT INTO final_status (evaluate, paper_id, author_id) VALUES (%s,%s,%s)",
        (
            evaluate,
            int(paper_id),
            int(author_id),
        ),
    )
    mysql.connection.commit()
    return redirect(url_for("chief_editor_page"))


@app.route("/chief_editor_page", methods=["GET", "POST"])
def chief_editor_page():

    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM final_status")
    final_status = curl.fetchall()

    result_status = {}
    for i in final_status:
        result_status[i["paper_id"]] = i["evaluate"]
    session["final_status"] = result_status

    if request.args.get("evaluate"):
        evaluate = request.args.get("evaluate")
        paper_id = request.args.get("paper_id")
        author_id = request.args.get("author_id")

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute(
            "INSERT INTO final_status (evaluate, paper_id, author_id) VALUES (%s,%s,%s)",
            (
                evaluate,
                int(paper_id),
                int(author_id),
            ),
        )
        mysql.connection.commit()

        return redirect(url_for("chief_editor_page"))

    if session["firstname"]:
        email = session["email"]
        firstname = session["firstname"]
        data = session["data"]
        final_status = session["final_status"]

        temp = {}
        for k, v in final_status.items():
            temp[int(k)] = v

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * from  papers1")
        papers = curl.fetchall()
        mysql.connection.commit()

        papers_data = {}
        for i in papers:
            papers_data[i["paper_id"]] = i
        return render_template(
            "chief_editor.html",
            firstname=firstname,
            data=data,
            final_status=temp,
            papers_data=papers_data,
        )
    else:
        redirect(url_for("login_chief_editor"))


@app.route("/info", methods=["GET"])
def info():  # database name is papers
    return render_template("info.html")


@app.route("/info1", methods=["GET"])
def info1():  # database name is papers
    return render_template("info1.html")


if __name__ == "__main__":
    sess = Session()
    sess.init_app(app)
    app.debug = True
    app.run()
