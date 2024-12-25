from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from handler import login_required, sorry
import sqlite3
import bleach

postb = Blueprint('postb', __name__,url_prefix='/post')

#looking for a specific post
#route not locked so every one can share and read said post
@postb.route('/<int:post_id>')
def display_post(post_id):
    # Query db for a single post a show it
    try:
        conn = sqlite3.connect('social.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM blog_posts WHERE id = ?",(post_id,))
        rows = cursor.fetchall()
        #same as previous route dif name to avoid confusion
        dictr = [dict(row) for row in rows]
        post = dictr[0]
        #minor cleanup to avoid cross-side headaches
        post["content"] = bleach.clean(post["content"])
        conn.close()
    except:
        sorry("try a valid post id")
    return render_template("post.html",post = post)

# here the user sees his own posts
@postb.route("/history",methods=['GET','POST'])
@login_required
def history():

    uid = session['user_id']
    conn = sqlite3.connect('social.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    #fetching user specific posts
    cursor.execute("SELECT * FROM blog_posts WHERE user_id = ?",(uid,))
    rows = cursor.fetchall()
    #turning response into a dict with column names
    posts = [dict(row) for row in rows]
    conn.close()
    return render_template("history.html",posts=posts)

@postb.route("/make",methods=['GET','POST'])
@login_required
def make():
    user_id = session['user_id']
    if request.method =="POST":
        #openning connection
        title = request.form.get("title")
        content = request.form.get("content")
        conn = sqlite3.connect('social.db')
        cursor = conn.cursor()
        #inserting the post
        cursor.execute("INSERT INTO blog_posts (title, content,user_id) VALUES (?,?,?)",(title,content,user_id))
        conn.commit()
        conn.close()
        flash('Entry was successfully added')
        return redirect("/")

    return render_template("make.html")


#delete a unwanted post
@postb.route("/delete/<int:post_id>",methods=['GET','POST'])
@login_required
def delete_post(post_id):
    
    # connecting to database
    conn = sqlite3.connect('social.db')
    cursor = conn.cursor()
    # deleting post
    cursor.execute("DELETE FROM blog_posts WHERE id = ?",(post_id,))

    #commiting to changes
    conn.commit()
    conn.close()

    flash('Entry was successfully removed')
    return redirect("/")