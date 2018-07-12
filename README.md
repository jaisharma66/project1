# Project 1

Web Programming with Python and JavaScript

ALL PACKAGES NECESSARY ARE JUST THE IMPORTS! (I hope!)

Hello! Welcome to my second project for the web programming course. This document is going to give a short overview of what each file does,
and how the program works together. The longest description will be of application.py. I am going to go through each function. In regards
to resources used, I heavily relied on the documentation, stack overflow. lecture source code, and the slack. Furthermore, David Nunez
met with me to help me solve major problems with my code. I am going to try to list as many links as I can, but there was over 100 easily,
so I will list 10/15 of the most recent ones to get the point across.
https://pythonprogramming.net/decorator-wrappers-flask-tutorial-login-required/
http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
https://stackoverflow.com/questions/15591620/flask-how-to-retrieve-session-data
https://stackoverflow.com/questions/32640090/python-flask-keeping-track-of-user-sessions-how-to-get-session-cookie-id
https://darksky.net/dev/docs#data-block
https://stackoverflow.com/questions/32640090/python-flask-keeping-track-of-user-sessions-how-to-get-session-cookie-id
https://stackoverflow.com/questions/7931984/check-if-a-sql-select-statement-returns-no-rows
https://www.python-course.eu/python3_inheritance.php
https://stackoverflow.com/questions/17534345/typeerror-missing-1-required-positional-argument-self
https://stackoverflow.com/questions/18940249/function-missing-2-required-positional-arguments-x-and-y
https://stackoverflow.com/questions/14254308/is-there-a-way-to-pass-variables-into-jinja2-parents
https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
https://stackoverflow.com/questions/24851569/else-invalid-syntax-python
https://stackoverflow.com/questions/3308510/destroy-session-in-pylons-or-python
https://stackoverflow.com/questions/3308510/destroy-session-in-pylons-or-python
https://www.programcreek.com/python/example/79006/flask.session.clear

def login_required(f):
This function is a decorator that I learned to code from the very first link, and makes sure that the user is logged in under a session
to access certain parts of the website.

def index():
This function is the function that loads when the the program is first loaded through flask. It loads the very first page allowing the user
to login, logout, or register.

def register():
This function takes the form field sections of the register page and processes them in such a way as to add them to the table containing user data.
It also checks if the user already exists, and whether the user leaves some sections of the form blank. If so, it reprompts them using a boolean variable
An SQL insert command is used to add and commit the changes to the database.

def login_r():
This function is simply a reprompt of the form, hence the _r

def login():
This function is used to log the user in using sessions by creating the proper session. It gets the information from the form, checks to
see if they are already in the database, and logs them in. Else, it reprompts the user.

def logout():
This function simply logs the user out and sends them back to the main page of the website.

def search():
This is the search function which recieves the information from the form and then sends the result to another form.

def search_info(zipcode):
The information is recieved by this function, wherein it searches a table for the matching values. If no such values exist, an error is raised.
Furthermore, the API key is selected from inside of this function, and the json information is transferred over the the template for display.

def comment(zipcode):
This function takes the location that is selected and allows the user to add a comment. There is a check to make sure that the user has not commented
multiple times within the function. It adds the comment to the table and allows for it to be displayed to all users that are using the page.

def api_zipcode(zipcode):
This function generates the API JSON required for any zip code presented. If an incorrect zipcode that is not found, then an exception is raised.

failure.html
A reprompt if the login fails

index.html
The main page with buttons routing to different parts as specified

layout.html
The layout of all subsequent templates. All child templates extend this.

login.html
Allows for the user to login and reprompts if they are incorrectly logging in

register.html
Registers the user through a forum

search.html
This provides the user with a form to search and displays the values that are found

search_info.html
Displays the weather and other attributes. Also has a comment box for users to comment on the page.