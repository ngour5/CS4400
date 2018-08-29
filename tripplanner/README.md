Trip Planner
===

Running the Web App
---

1. If you don't already have them, install Python 3 and pip.
2. Clone this repository to your computer.  These instructions will assume you clone it to a directory
called `trip-planner`.
3. Switch to the `trip-planner` directory.
4. Create a virtual environment to contain this project.  The way you do this will vary depending on your operating system:
   
   a. Windows: Run `py -3 -m venv venv`
   
   b. Mac: Run `python3 -m venv venv`
5. Activate the virtual environment.  Run the appropriate command for your OS:
   
   a. Windows: Run `venv\Scripts\activate`
   
   b. Mac: Run `. venv/bin/activate`
6. Look for a `(venv)` at the beginning of each new line in your terminal.  This means you're
in your virtual environment.
7. Run `pip install -r requirements.txt` to install the dependencies.
8. Copy the `.env.example` file to `.env` and add the required values by following the directions
in the files.
9. Run `team11-schema.sql` and `team11-data.sql` to setup and add starter data to the database.
10. Start the webserver by running `flask run` inside the virtual environment.
11. You can access the application at [127.0.0.1:5000](127.0.0.1:5000) or [localhost:5000](localhost:5000).
12. Sign in with the following credentials, or create your own account:

a. Administrator: admin@example.com / password

b. User: someone@example.com / password
   

Project Structure
===
This repository contains 3 main things:
1. SQL files for setting up the database
2. Flask server (backend) files
3. HTML (frontend) files

Prerequisites to run the webserver:

- Make sure you have all of the dependencies (see **Installing the dependencies**, below)




Installing the dependencies
===
1. Make sure you have Python 3
2. Open a shell (Terminal or Command Prompt) and navigate to the `trip-planner` directory
3. Create a virtual environment to contain this project.  The way you do this will vary depending on your operating system:
   
   a. Windows: Run `py -3 -m venv venv`
   
   b. Mac: Run `python3 -m venv venv`
4. Every time you want to work with Python in this project, you need to activate the virtual environment.  Run the
appropriate command for your OS:
   
   a. Windows: Run `venv\Scripts\activate`
   
   b. Mac: Run `. venv/bin/activate`
5. Look for a `(venv)` at the beginning of each new line in your terminal.  This means you're
in your virtual environment.
6. Run `pip install -r requirements.txt` to install Flask and the other required Python packages.
   
   
Setup PyCharm
===

### Virtualenv
1. Go to **Settings** > **Project: trip-planner** > **Project Interpreter** in PyCharm and follow these instructions so it'll recognize your virtual environment:
2. In the Project Interpreter dropdown menu, select **Show all...**.
3. A list of project interpreters appears.  Click the **+** on the right-top area of this window.
4. Another new window opens.  Make sure **Virtualenv Environment** is selected in the left sidebar.  In the main area of this window, choose **Existing environment**.
5. For **Interpreter:**, the default option should be what you want.  Make sure the path listed there includes "trip-planner."  [This is because Virtualenv has its own Python executable inside the `venv` directory.  That's what we're telling PyCharm about in this step.]
6. Click OK 2 times to go back to the main Settings window.
7. A list of packages and versions should appear in the Settings window.
8. PyCharm should now recognize Flask.

### Flask run configuration
1. You can run the Flask webserver directly through PyCharm.
2. Look in the top right of PyCharm for a blank dropdown menu near a green play button.
3. Click the dropdown menu and click **Edit Configurations...**
4. In the top left of the window that opens, click the **+**
5. Choose **Flask** in the list of options that appears
6. For Name, enter **Planner**
6. For Target type, choose **Module name**
7. For Target, enter **planner.py**
8. FLASK_ENV is **development**
9. Check the box next to FLASK_DEBUG
10. Verify that **Python Interpreter** contains "trip-planner" (this indicates that PyCharm will run the webserver in your
virtual environment)

### Tell PyCharm about templates
1. On the left pane of PyCharm where all the files are listed, right click on the **templates** directory
2. Click **Mark Directory As** and choose **Template folder**

Setup .env
===
1. The .env file tells Flask some important details like your database username and password that you wouldn't want to commit to GitHub for security reasons.
2. Copy .env.example to a new file called `.env`
3. Follow the instructions inside .env

Run the development server
===
1. Make sure Planner is selected in the Run dropdown menu in the top right of PyCharm.
2. Click the green play button.
3. Visit the web app at the URL listed or localhost:5000

What's Where?
===

Here's a breakdown of the structure of the Flask project:
1. `planner.py` contains all of the HTTP routes.  That is, this is where what happens when you visit every
page on the website is defined.
2. Some of the functions in `planner.py` are organized into `auth.py` and `util.py` to keep everything organized.
3. `templates` contains the actual HTML used.  Note that there isn't one HTML page for every distinct page on the website.
Instead, a templating engine called Jinja is used.  This reduces repetition of boilerplate code such as the navigation bar.
4. `templates/include` includes some of the HTML foundations used by other pages.

