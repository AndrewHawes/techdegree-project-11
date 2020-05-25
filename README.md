# Pug or Ugh
Project 11 of the Python Web Development Techdegree program

This project uses a REST API built with Django Rest Framework for a React app
that allows users to browse a selection of dogs. 

Users can: 

- set multiple selection criteria that automatically filter the dogs
- save decisions on which dogs they like and dislike (pug or ugh)
- add and delete their own dogs

## Installation

You'll need Node.js and NPM to install and run this project.
The React app and Django will be run on separate ports.

_If you haven't installed Node.js, you can find instructions at
[How to Install Node.js and NPM on Windows](https://blog.teamtreehouse.com/install-node-js-npm-windows)._

###I. Set up the Django back end

1. Download the project and change into the project directory.
2. Create a new virtual environment 
    - Windows: `python -m venv env` 
    - Linux/Mac `python3 -m venv env`
3. Activate the virtual environment
    - Windows: `.\env\Scripts\activate`
    - Linux/Mac: `source env/bin/activate`
4. Install the project's Python dependencies.
    - `pip install -r requirements.txt`
5. Run migrations to initialize the database.
    - `python manage.py migrate` 
6. Run `data_import.py` to populate the database.
    - `python data_import.py` 
    (You will see a success message once data has loaded.)
    
###II. Set up the React front end 

1. Change into the frontend directory.
    - `cd frontend`
2. Use NPM to install the project's Javascript dependencies.
    - `npm install`

###III. Run the project

Assuming nothing went horribly wrong with the last step, you should now be able
to run everything. You'll be running Django on port 8000 and React on port 3000.

1. Go back to the main project directory and start the Django test server.
    (Make sure you're still in your virtual environment.)
    - `python manage.py runserver`
    (It needs to be running on port 8000, but it should do that automatically.)
2. Open another terminal window, and change into the frontend directory.
    - `cd frontend`
3. Start the Node server. It should start on port 3000.
    - `npm start`
4. This should open a new browser tab automatically, but if not, 
open your browser and go to [127.0.0.1:3000](127.0.0.1:3000) to use the app.

