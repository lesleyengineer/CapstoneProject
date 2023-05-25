# Capstone Final Project

## Lesley Ferrie



## Please note tokens will expire at 3pm on 25/05/2023

Info - Thank you for taking the time to look at my project.  This is an api built as part of my final capstone project through udacity.  

Motivation - I choose to do the casting agency project as I felt like the guidance through udacity would give me the support that I needed to complete the project.  I also really enjoy movies so thought this would be a fun way to learn.  I have found the piecing together of everything we learned in the previous 4 projects to be very challenging but also very rewarding.



# WELCOME TO HOLLYWOOD CASTING AGENCY!!!

Our casting agency prides itself on bringing the newest talent to the big screen!!

##############################################################################################



## SET UP

1. Python 3.9 - Follow instructions to install the latest version of python for your platform in the python docs

2. Virtual Environment - This keeps your dependencies for each project separate and organised. Instructions for setting up a virual environment for your platform can be found in the python docs

3. PIP Dependencies - Once you have your virtual environment setup and running, install dependencies:

4. pip install -r requirements.txt

5. Environment Variables You will first need to populate your setup.sh script with your own database credentials

6. Run setup.sh script to set up your database environment variables as well as the auto0 parameters and JWT TOKEN for test_app.py.



## DATABASE SET UP

Run postgres locally and create a local database called casting-agency
-- createdb cating-agency --
The database will pre populate with data from movie-options.py on the first run.



## AUTH0 SETUP

1. Access auth0 via https://auth0.com/
2. Set up new account with email and password
3. Select a unique tenant domain
4. Create a new single page web domain via the 'create application' button
5. Create a new API and choose to enable RBAC and add permissions via the setting section
6. Create new API permissions 
    - add actors
    - add movie
    - get actor
    - get movie
    - patch actor
    - patch movie
    - delete actor
    - delete movie
7. Create new roles for all 3 people 
    - casting assistant can get(view) both actors and movies from the database.
    - casting director can get(view) both actors and movies, post(create) or delete an actor and patch(edit) actors and movies from the database.
    - executive producer can get(view) both actors and movies, post(create) or delete actors and movies, patch(edit) actors and movies and also delete both actors and movies from the database.



## AUTH0 LOGINS

website - https://nanofs.uk.auth0.com/authorize?

audience=http://localhost:5000&
    response_type=token&
    client_id=6M6yvm9pW3BzeoOGvq7uorlgCBQyOo1v&
    redirect_uri=http://localhost:8100

    casting assistant
    email - castingassistant@hollywood.com
    password - hollywood1!
    permissions - the casting assistant has the permission to get(view) both actors and movies from the database.

    casting director
    email - castingdirector@hollywood.com
    password - hollywood1!
    permissions - the casting director has the permission to get(view) both actors and movies, post(create) or delete an actor and patch(edit) actors and movies from the database.

    executive producer
    email - executiveproducer@hollywood.com
    password - hollywood1!
    permissions - the executive producer has the permission to get(view) both actors and movies, post(create) or delete actors and movies, patch(edit) actors and movies and also delete both actors and movies from the database.

The app has been deployed at - https://hollywood-casting-agency.onrender.com



## API's 

GET/movies

- this will get and display a list of movies showing the title and release_year
- request arguments: none

example 

{
    "movies": [
        {
            "actors": [],
            "id": 1,
            "release_year": "1974",
            "title": "The Movie6"
        },
        {
            "actors": [],
            "id": 2,
            "release_year": "1992",
            "title": "Little Bnanas"
        }
    ],
    "success": true
}

GET/actors

- this will get and display a list of actors showing the name, age and gender
- request arguments:none

example

{
    "actors": [
        {
            "age": 28,
            "id": 1,
            "movies": [],
            "name": "Peter Panto"
        },
        {
            "age": 30,
            "id": 2,
            "movies": [],
            "name": "Peter Piper"
        }
    ],
    "success": true
}


POST/movies

- this will create a new movie and add it to the database
- request arguments: title, release year

example

{
    "movie": {
        "actors": [],
        "id": 3,
        "release_year": "1965",
        "title": "The Funny Girl"
    },
    "posted": 3,
    "success": true
}

POST/actors

- this will create a new actor and add them to the database
- request arguments: name, age, gender

example

{
    "actor": {
        "age": 38,
        "id": 3,
        "movies": [],
        "name": "Peter Pillow"
    },
    "created": 3,
    "success": true
}

PATCH/movies/<movie-id>

- this will edit an existing movie and update the database
- request arguments: OPTIONAL title, release year

example

{
    "movie": {
        "actors": [],
        "id": 3,
        "release_year": "1965",
        "title": "the best movie ever"
    },
    "success": true
}


PATCH/actors<actor-id>

- this will edit an existing actor and update the database
- request arguments: OPTIONAL name, age, gender

example

{
    "actor": {
        "age": 30,
        "id": 2,
        "movies": [],
        "name": "Tina Teapotterson"
    },
    "success": true
}

DELETE/movies/<movie-id>

- this will delete an exisitng movie and remove from the database
- request arguments:movie_id

{
    "deleted": 3,
    "success": true
}

DELETE/actors<actor-id>

- this will delete an exisitng actor and remove from the database
- request arguments:actor_id

{
    "deleted": 2,
    "success": true
}


Error codes

- 400: bad request
- 404: not found
- 422: unprocessable content
- 500: internal server error








