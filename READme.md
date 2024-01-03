# Warbler - A Twitter Clone

This exercise is intended to extend a somewhat-functioning Twitter clone. It was intended to give me practice reading and understanding an existing application, as well as fixing bugs in it, writing tests for it, and extending it with new features.

## Setup

To get this application running, make sure you do the following in the Terminal:

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `createdb warbler`
5. `createdb warbler-test`
6. `python3 seed.py`


## Part 1 Fix Current Features
1. Undersatnding the Model:  
The follows table has 2 foreign keys because a row is created with two different user_ids taken fromt he users table
<br/>

2. Fixed Logout route and added a flash message when logged out successfully
<br/>

3. Fixed User Profile to show the correct location, bio, and header image
<br/>

4. Fixed the User Cards to show the correct bio information
<br/>

5. Added Edit Profile functionality
<br/>

6. Fixed the Homepage to show the last 100 warbles only from the users that the logged-in user is following, and that user, rather than warbles from all users.
<br/>

7. researched and understood login strategy  
- How is the logged in user being kept track of?  
It is being tracked throught the flask global object called g.
- What is Flask’s ***g*** object?  
The g object is flask global object which can be accessed in requests
- What is the purpose of ***add_user_to_g ?***  
The purpose of this function is to check if a user has loged in through the sessions[CURR_USER_KEY]. If they are logged in then the user gets added to global object so it can be accessed in the routes.
- What does ***@app.before_request*** mean?  
This function is performed before every request, so the global oject can be up to date for every request.

## Part 2
I added a Like Message functionality without using AJAX or javascript.

## Part 3
Added Tests for the Models and views


