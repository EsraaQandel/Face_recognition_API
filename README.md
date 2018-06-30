# Project Overview

This is an API based on the *[Face_recognition](https://github.com/ageitgey/face_recognition)* project by *[Adam](https://github.com/ageitgey)*

### Requiremnets 

1- Install the dependency libraries (Flask, sqlalchemy, requests and face_recognition)

2- Install postgreSQL 



## Running the App

-Create a database with the name **list** through psql (owner:postgres, pass:postgres), this *[postgresql-command-line-cheat-sheet](https://blog.jasonmeridth.com/posts/postgresql-command-line-cheat-sheet/)* is very helpful.

-if you already have the db you can connect to it by:

  `sudo -u postgres psql`
  `postgres=# \c list`

-Now type **python3 database_setup.py** in CMD to initialize the database.

-Type **python3 service.py** in CMD to run the Flask web server.

  
