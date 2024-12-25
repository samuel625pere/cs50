# Final Project: SAM's tree house

## introduction

### inspiration

For this project I elected to try and make my own blog page
my inspiration was the old web pages that were available
in the 2000's where you could post on blogs and add you own touch.

I had a bit of knowledge on PHP, so I decided to try flask for this.

### dividing the script

During development I realized the main script would be too big 
and went to the documentation on how to handle the routes,
afterall aside from the registration i'd also would have to add
the routes for the posts and displaying them, so i did it using
the blueprint functionality of flask, plus a little inspiration from finance.

## The application

### Tools used

The application was edited using visual studio code with the help of the windows WSL
using ubuntu and the linux distro.

The language used for the scripts was python, alongside the [Flask](https://flask.palletsprojects.com/en/latest/) library,
as a framework for a webserver.

The html pages were designed using bootstrap 5 
and in order to simplify and streamline their look Jinja 2 was used for both its
functionality for creating layouts and displaying the requested data from the database.

To supply the application a database was made in sqlite3 and was connected to it
by the python sqlite3 library throughout the application.
The bleach library was used to sanitize any code with probable malicious
application.

As for non code tools: the favicon was picked from icons8, and the grumpy cat
meme was sourced from imgur and generated using [memegen](https://github.com/jacebrowning/memegen) api.

### handler.py

The above script contains one function to only allow a logged user
in user-specific routes and another, that was inspired on week 9 finance,
that leads to error specific display page with my own grumpy cat meme.

The "sorry()" function escapes special characters for the memegen API request,
the API request in the sorry.html page will display a grumpy cat with
a error message pertaining to the function misused.

The latter function "login_required(f)" is a decorator function,
where f are all arguments for any route in the application,
this decorator redirects any unauthenticated access to the login page.

### app.py

In the main script I decided to work the handling of user trafic
the index, registration, login and logout since they we're major concerns.
the mechanism as a whole is powered by the security set of functions
from werkzeug.

Index shows the user latest the posts, that is done by quering the database
for all posts ordering them by desending order `SELECT * FROM blog_posts ORDER BY timestamp DESC`.
The route view in index.html organizes this as a table with a button in each line
for the user to view the post.

Login when requested by a GET method ,will display the login.html
page where the user is prompted to send a form with username and
password to the same route via POST method, if so the function will
select query and check to validity of the credentials, a valid entry
will log the user and redirect to the main page flashing a confirmation message,
otherwise the user receives a error page asking for proper login credentials.

Register route if prompted by a GET method will return the register.html
where the user must fill the form with a chosen username, a password and a email,
the form sends the info to the route via POST method, where the password get's converted
into a hash for security and the information in the form is added to the database
in a insert query and the user is redirected to the index page.

Finally the logout route simply clears the session and
redirects the user to the index page flashing a confirmation message.

### postm.py

In this script I have elected to house the post related routes.

I't has a display route (not restricted by design) were users
can see specific posts if the have the posts ID, since the text can be a html
this route has the clean function from bleach to stop cross-site scripting.

A history route the script function 
queries the database for the authenicated user posts
so users can see and delete their own posts with ease
in a single page, with a single button.

The make route handles the posting of new posts, the function
makes a INSERT request for the database with the post title,
content and adds it as a new line in the database.

The delete route removes a post from the database, the function
sends a DELETE request for the database with the post id as identifier and then
redirects to index route flashing a confirmation message.

### social.db

This database was made in sqlite3 and has 2 relevant tables: users and blog_posts
(sqlite_sequence is for handling sequencing of the index numbers).

The users table holds the account id(uid, integer), username(username, text), password hash(hash, text)
and the e-mail(email, text) of a user.

The blog_posts table holds the primary key (id, integer), the post title (title, text), it's content(content, text),
the timestamp(timestamp, timestamp) of when it was posted and the user id of author(user_id, integer) of the
post as foreign key. 

### style.css

Simple css script to style the big index LOGO.