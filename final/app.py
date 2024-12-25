
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from handler import login_required, sorry
from postm import postb
import sqlite3


app = Flask(__name__)
app.register_blueprint(postb)

if __name__ == '__main__':
    app.run()

#taking a tip out of week 9 finance and using filesystem instead of signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    conn = sqlite3.connect('social.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blog_posts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    #same as previous route dif name to avoid confusion
    posts = [dict(row) for row in rows]
    conn.close()
    return render_template("index.html",posts=posts)

#the folowing routes pertain user registration
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #getting password hash
        conn = sqlite3.connect('social.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT uid,hash FROM users WHERE username = ?",(username,))
        rows = cursor.fetchall()
        print(rows)
        #turning response into a dict with column names
        user = [dict(row) for row in rows]
        print(user)
        conn.close()
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return sorry("Please enter a valid username and password")
        else:
            #remember logged user
            print(user)
            session["user_id"] = user[0]["uid"]
            flash('You\'re logged in!')
            return redirect("/")
        
    else:
        return render_template("login.html")


#registration route for app
@app.route("/register",methods=['GET','POST'])
def register():
    #toss away any user info
    session.clear()

    if request.method == "POST":
        #check all required fields on the form
        username = request.form.get("username")
        if not username:
            return sorry("Please enter a valid username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation:
            return sorry("Enter a valid password and confirm it")
        elif password != confirmation:
            return sorry("Password and confirmation don't match")
        email = request.form.get("email")
        if not email:
            return sorry("add a email")
        
        #database handling
        """
        note to mind: make a specialized set of functions for this later
        must find way to not clog main script with this lines
        """
        conn = sqlite3.connect('social.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, hash, email) VALUES (?,?,?)",(username,generate_password_hash(password),email))
        conn.commit()
        conn.close()
        #print(username,password,confirmation,email)
        return render_template("index.html")
    else:
        return render_template("register.html")
    

@app.route('/logout',methods=['GET','POST'])
def logout():
    #clear session
    session.clear()
    #bring user back to main page
    flash('You\'re logged out!')
    return redirect("/")