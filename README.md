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
as a framework for a webserver, the pages were designed using bootstrap 5
for the looks and flask's compatibity with jinja to streamline looks
and display the data, the database was made in sqlite3 and was connected to it
by the python sqlite3 library throughout the application.
The bleach library was used to sanitize any code with probable malicious
application.

As for non code tools: the favicon was picked from icons8, and the grumpy cat
meme was sourced from imgur and generated using [memegen](https://github.com/jacebrowning/memegen) api.

### handler.py

The above script contains one function to only allow a logged user
in user-specific routes and another, that was inspired on week 9 finance,
that leads to error specific display page with my own grumpy cat meme.

### app.py

In the main script I decided to work the handling of user trafic
the index, registration, login and logout since they we're major concerns.
the mechanism as a whole is powered by the security set of functions
from werkzeug.

Index shows the user latest the posts, the remainder are simple registration,
login and logout mechanisms for the page. 

### postm.py

In this script I have elected to house the post related routes.

I't has a display route (not restricted by design) were users
can see specific posts if the have the posts ID, since the text can be a html
this route has the clean function from bleach to stop cross-site scripting.

A history route so users can see and delete their own posts 
in a single page, with a single button.

The make route handles the posting of new posts.

The delete route removes a post from the database,
redirects to index route and flashes a confirmation message.

### social.db

This database was made in sqlite3 and has 2 relevant tables: users and blog_posts
(sqlite_sequence is for handling sequencing of the index numbers).

The users table holds the account id, username, password hash and the e-mail
of a user.

The blog_posts table holds the post id, the post title, it's content,
the timestamp of when it was posted and the user id of author of the
post.