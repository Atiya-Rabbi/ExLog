import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import json
import requests
from bs4 import BeautifulSoup

from helpers import apology, login_required, to_json

# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
user = 0


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///user.db")
search = "false"
user_id = 0


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Render map"""
    if request.method == "POST":
        if str(request.form.get('search')):
            global search
            search = str(request.form.get('search'))

            r = requests.get(url="http://localhost:8082/" + str(session['user_id']), json='true')
            print(type(r.status_code))
            if r.status_code == 500:
                return apology("Request timed out, refresh the page", 408)
            articles = r.json()
            length = len(articles)
            sObject1 = slice(length // 2)
            sObject2 = slice(length // 2, length)
            article1 = articles[sObject1]
            article2 = articles[sObject2]
            length1 = len(article1)
            length2 = len(article2)
            data = db.execute("SELECT username, name, dp FROM users WHERE id=:Id", Id=session["user_id"])
            interests = db.execute("SELECT interests FROM interest WHERE id=:Id", Id=session["user_id"])
            first = data[0]['name'].split(" ")
            if not data[0]['username']:
                username = '@' + data[0]['name'].replace(" ", "")
            else:
                username = '@' + data[0]['username']
            show = "true"

            return render_template("index.html", length1=length1, length2=length2, article1=article1, article2=article2, show=show, image=data[0]['dp'], name=first[0], username=username, interests=interests)
        else:
            flash("Interest Not Selected")
            return apology("Sorry nothing to Show", 400)
    else:

        update = db.execute("update users set count=:count where id=:Id",
                            count=1, Id=session["user_id"])
        # sends request for data of link preview with session id as parameter
        url = "http://localhost:8082/" + str(session['user_id'])
       # url2="http://ide50-atiya-rabbi.cs50.io:8080/url/"+ str(session['user_id'])
       # print(url)
       # print(url2)
       # r=requests.get(url2)

        r = requests.get(url)
        print(type(r.status_code))
        if r.status_code == 500:
            return apology("Request timed out, refresh the page", 408)
        # recieve data of link preview
        articles = r.json()
        length = len(articles)
        sObject1 = slice(length // 2)
        sObject2 = slice(length // 2, length)
        article1 = articles[sObject1]
        article2 = articles[sObject2]
        length1 = len(article1)
        length2 = len(article2)
        # print(length1,length2)

        data = db.execute("SELECT username, name, dp FROM users WHERE id=:Id", Id=session["user_id"])
        # print("im done")
        interests = db.execute("SELECT interests FROM interest WHERE id=:Id", Id=session["user_id"])
        first = data[0]['name'].split(" ")
        if not data[0]['username']:
            username = '@' + data[0]['name'].replace(" ", "")
        else:
            username = '@' + data[0]['username']
        show = "true"

        return render_template("index.html", length1=length1, length2=length2, article1=article1, article2=article2, show=show, image=data[0]['dp'], name=first[0], username=username, interests=interests)


# send urls of site based  on intrest
@app.route("/url/<user_id>", methods=["GET", "POST"])
def url(user_id):
    url = []
    global search
    if search != "false":
        if search == 'science':
            url.append("https://www.livescience.com/news")
        elif search == 'politics':
            url.append("https://edition.cnn.com/specials/politics/world-politics")
        elif search == 'business':
            url.append("https://www.wired.co.uk/topic/business")
        elif search == 'entrepreneurship':
            url.append("https://hbswk.hbs.edu/Pages/browse.aspx?HBSTopic=Entrepreneurship")
        elif search == 'technology':
            url.append("https://www.wired.co.uk/topic/technology")
        elif search == 'writing':
            url.append("https://www.everywritersresource.com/on-writing")
        elif search == 'entertainment':
            url.append("https://hellogiggles.com/reviews-coverage")
        elif search == 'fashion':
            url.append("https://hellogiggles.com/fashion")
        elif search == 'health':
            url.append("https://www.ideafit.com/fitness-library")
        elif search == 'self':
            url.append("https://www.pickthebrain.com/blog/self-improvement-articles")
        search = "false"
        return jsonify(url)

    else:

        interests = db.execute("SELECT interests FROM interest WHERE id=:Id", Id=int(user_id))
        if not interests:
            platform1 = "https://edition.cnn.com/specials/politics/world-politics"
            url.append(platform1)
            platform2 = "https://hellogiggles.com/reviews-coverage"
            url.append(platform2)
            platform3 = "https://www.wired.co.uk/topic/technology"
            url.append(platform3)

            return jsonify(url)
        else:
            for interest in interests:
                interests = interest["interests"]
                if interests == 'science':
                    url.append("https://www.livescience.com/news")
                elif interests == 'politics':
                    url.append("https://edition.cnn.com/specials/politics/world-politics")
                elif interests == 'business':
                    url.append("https://www.wired.co.uk/topic/business")
                elif interests == 'entrepreneurship':
                    url.append("https://hbswk.hbs.edu/Pages/browse.aspx?HBSTopic=Entrepreneurship")
                elif interests == 'technology':
                    url.append("https://www.wired.co.uk/topic/technology")
                elif interests == 'writing':
                    url.append("https://www.everywritersresource.com/on-writing")
                elif interests == 'entertainment':
                    url.append("https://hellogiggles.com/reviews-coverage")
                elif interests == 'fashion':
                    url.append("https://hellogiggles.com/fashion")
                elif interests == 'health':
                    url.append("https://www.ideafit.com/fitness-library")
                elif interests == 'self':
                    url.append("https://www.pickthebrain.com/blog/self-improvement-articles")
            return jsonify(url)


# this is forgot password
@app.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        global user
        user = str(request.form.get("username"))
        ff = str(request.form.get("firstfriend"))
        fb = str(request.form.get("favouritebook"))
        check = db.execute("SELECT firstfriend,favouritebook FROM users WHERE username=:user", user=user)

        if check[0]["firstfriend"] == ff and check[0]["favouritebook"] == fb:

            return redirect("/recover")

        else:
            flash("security questions/Username don't match")
            return render_template("forgot_password.html")
    else:
        return render_template("forgot_password.html")


# this is recover
@app.route("/recover", methods=["GET", "POST"])
def recover():
    global user
    if session.get("user_id"):
        user = db.execute("select username from users where id=:Id",
                          Id=session["user_id"])
        user = user[0]["username"]
    if request.method == "POST":
        newpass = str(request.form.get("new"))
        # print(newpass)
        confirm = str(request.form.get("confirmation"))
        # print(confirm)
        if newpass == confirm:
            db.execute("update users set hash=:hash where username=:username",
                       hash=generate_password_hash(newpass), username=user)
            user = 0
            return redirect("/")
        else:
            flash("passwords mismatch")
            return render_template("recover.html")
    else:
        if session.get("user_id") != None:
            data = db.execute("SELECT dp, name FROM users WHERE id=:Id",
                              Id=session['user_id'])
            return render_template("recover.html", image=data[0]['dp'], name=data[0]['name'])
        else:
            return render_template("recover.html")


# this is profile section
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Render Profile"""
    dp = db.execute("select dp,username,count,name from users where id=:Id",
                    Id=session["user_id"])
    if request.method == "POST":
        dp = str(request.form.get("encodedImg"))
        ff = str(request.form.get("firstfriend"))
        fb = str(request.form.get("favouritebook"))
        ins = []
        ins.append(str(request.form.get("business")))
        ins.append(str(request.form.get("entrepreneurship")))
        ins.append(str(request.form.get("politics")))
        ins.append(str(request.form.get("science")))
        ins.append(str(request.form.get("technology")))
        ins.append(str(request.form.get("entertainment")))
        ins.append(str(request.form.get("writing")))
        ins.append(str(request.form.get("health")))
        ins.append(str(request.form.get("self")))
        ins.append(str(request.form.get("fashion")))
        check = db.execute("DELETE from interest where id=:Id",
                           Id=session["user_id"])
        for i in range(0, 10):
            if ins[i] != None:

                if check:
                    db.execute("insert into interest(id,interests) values(:Id,:interest)", Id=session["user_id"], interest=ins[i])
                else:
                    db.execute("insert into interest(id,interests) values(:Id,:interest)", Id=session["user_id"], interest=ins[i])

        count = db.execute("SELECT count FROM users WHERE id=:Id",
                           Id=session["user_id"])
        count = count[0]["count"]

        if dp != "":
            db.execute("update users set dp=:dp where id=:Id",
                       dp=dp, Id=session["user_id"])
        if count == 0:
            db.execute("update users set firstfriend=:ff, favouritebook=:fb WHERE id=:Id",
                       ff=ff, fb=fb, Id=session["user_id"])
        return redirect("/")
    uname = dp[0]["username"]
    if not uname:
        uname = "@" + dp[0]["name"]
        return render_template("profile.html", image=dp[0]["dp"], count=dp[0]["count"], uname=uname, name=dp[0]["name"])
    else:
        return render_template("profile.html", image=dp[0]["dp"], count=dp[0]["count"], uname=dp[0]["username"], name=dp[0]["name"])


# this is route to privacy policy
@app.route("/privacy", methods=["GET"])
def privacy():
    if session.get("user_id") != None:
        data = db.execute("SELECT dp, name FROM users WHERE id=:Id",
                          Id=session['user_id'])
        return render_template("/privacy_policy.html", image=data[0]['dp'], name=data[0]['name'])
    else:
        return render_template("/privacy_policy.html")


# this is sign in section
@app.route("/signin", methods=["GET", "POST"])
def signin():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not str(request.form.get("username")):
            flash("must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not str(request.form.get("password")):
            flash("must provide password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=str(request.form.get("username")))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], str(request.form.get("password"))):
            flash("invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        user_id = session["user_id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("/login.html")


# this is sign out section
@app.route("/signout")
def signout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# this is sign up secion
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not str(request.form.get("name")):
            flash("must provide name")
            return render_template("register.html")

        # Ensure username was Submitted
        elif not str(request.form.get("username")):
            flash("must provide username")
            return render_template("register.html")

        # Ensure password was submitted
        elif not str(request.form.get("password")):
            flash("must provide password")
            return render_template("register.html")

        # Ensure passwords match
        elif not str(request.form.get("confirmation")) == str(request.form.get("password")):
            flash("passwords don't match")
            return render_template("register.html")

        # implementation of correct usage
        else:
            hash = generate_password_hash(str(request.form.get("password")))
            result = db.execute("INSERT INTO users (name, username, hash) VALUES(:name, :username, :hash)",
                                name=str(request.form.get("name")), username=str(request.form.get("username")), hash=hash)

            if not result:
                flash("username already taken!")
                return render_template("register.html")
            else:
                # Remember which user has logged in
                session["user_id"] = result
                flash("Registered Successfully!")
                # Redirect user to home page
                return redirect("/profile")

    # ensure user to input via POST
    else:
        return render_template("/register.html")


# this is fb login section
@app.route("/fblogin", methods=["POST"])
@to_json
def fblogin():
    data = request.get_json()
    jsonToPython = json.dumps(data)
    jsonToPython = json.loads(jsonToPython)
    name = jsonToPython["username"]
    email = jsonToPython["email"]
    Id = jsonToPython["id"]
    dp = jsonToPython["dp"]
    if not email:
        email = Id
    check = db.execute("select dp,id from users where fbid=:Id AND email=:email",
                       Id=Id, email=email)
    if not len(check) == 1:
        new = db.execute("INSERT INTO users(fbid, email, name, dp) VALUES(:Id, :email, :name, :dp)",
                         Id=Id, email=email, name=name, dp=dp)
        if new:
            session["user_id"] = new
            user_id = session["user_id"]
            return "yes"
        else:
            return redirect("/signin")
    else:
        if check[0]["dp"] != dp:
            update = db.execute("update users set dp=:dp where id=:Id",
                                dp=dp, Id=Id)
        session["user_id"] = check[0]["id"]
        user_id = session["user_id"]
        return "exist"


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)