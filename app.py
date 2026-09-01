# Flask: The web framework that handles HTTP requests and responses
# render_template: A function that reads HTML files and fills in variables
from flask import Flask, render_template

# SQLAlchemy: The ORM (Object-Relational Mapper) that connects Python to databases
# It maps Python classes to database tables and Python objects to rows
from flask_sqlalchemy import SQLAlchemy

# datetime.utcnow() to track when records are created
from datetime import datetime

# Using for reading environment variables (like secret keys)
import os


# Flask uses __name__ to find where templates and static files are located
app = Flask(__name__)


# =============================================================================
# CONFIGURATION - Settings for our application
# =============================================================================

# SECRET_KEY is used for:
# 1. Signing cookies so Flask knows they haven't been tampered with
# 2. CSRF protection (prevents cross-site request forgery attacks)
# 3. Generating secure session IDs

# ! Change and store in .env later
app.config['SECRET_KEY'] = 'asfsa-ahe432-eghiwe-235e'

# SQLALCHEMY_DATABASE_URI tells SQLAlchemy WHERE your database is and HOW to connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_tracker.db'

# Set to false to disable tracking every change to every object
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# =============================================================================
# DATABASE INITIALIZATION - Creating the database connection
# =============================================================================

# Create the SQLAlchemy database object and bind it to our Flask app
#   db.Model      - The base class for defining database models
#   db.Column     - Defines columns (fields) in our tables
#   db.session    - The connection to the database (like a workspace)
#   db.create_all() - Creates all defined tables in the database
db = SQLAlchemy(app)


# =============================================================================
# DATABASE MODEL - Defining what a "Job Application" looks like in the database
# =============================================================================

# db.Model means: "This is a database model"
class Application(db.Model):
    
    # --- COLUMN 1: Primary Key (unique ID for each row) ---
    # 
    # This is a unique identifier for each application
    # 
    # primary_key=True: This is the primary key (unique, auto-incremented)
    # 
    # What this does: When you add a new Application, SQLAlchemy automatically
    # sets id to 1, 2, 3, etc. You don't need to specify it yourself.

    id = db.Column(db.Integer, primary_key=True)
    
    # --- COLUMN 2: Company Name ---
    # 
    # db.String(200):  This is text with a maximum length of 200 characters
    # nullable=False:  This field cannot be empty (must have a value)

    company_name = db.Column(db.String(200), nullable=False)
    
    # --- COLUMN 3: Job Title ---
    # 
    # db.String(200):  Text with max length of 200 characters
    # nullable=False:  Must have a value (cannot be empty)
    # 
    # Example: "Software Engineer", "Product Manager", "Data Scientist"

    job_title = db.Column(db.String(200), nullable=False)
    
    # --- COLUMN 4: Application Status ---
    # 
    # db.String(50):   Text with max length of 50 characters
    # nullable=False:  Must have a value
    # default='Applied': If no status is provided, automatically set to 'Applied'
    # 
    # Status options:
    #   'Applied'      - Application submitted, waiting to hear back
    #   'Phone Screen' - You have a phone interview scheduled
    #   'Interview'    - You have an in-person or video interview
    #   'Offer'        - You received a job offer
    #   'Rejected'     - Your application was rejected
    #   'Withdrawn'    - You withdrew your application

    status = db.Column(db.String(50), nullable=False, default='Applied')
    
    # --- COLUMN 5: Date Applied ---
    # 
    # db.DateTime:     Stores both date AND time
    # default=datetime.utcnow: If no date is provided, use the current UTC time
    # 
    
    date_applied = db.Column(db.DateTime, default=datetime.now)
    
    # --- COLUMN 6: Created At (when this record was created in the database) ---
    # 
    # db.DateTime:     Stores both date and time
    # default=datetime.utcnow: If not specified, use the current time
    # 
    # Note: This is DIFFERENT from date_applied
    #   date_applied:  When you submitted the job application
    #   created_at:    When you added this record to YOUR database

    created_at = db.Column(db.DateTime, default=datetime.now)


# =============================================================================
# ROUTE 1: Home Page (Hello World)
# =============================================================================

# @app.route('/') is a DECORATOR that tells Flask:
# 
# If you wanted a different URL, you'd change the path:
#   @app.route('/applications')     -> http://localhost:5000/applications
#   @app.route('/reports')          -> http://localhost:5000/reports
#   @app.route('/about')            -> http://localhost:5000/about

@app.route('/')
def hello():
    """
    This function runs when someone visits the homepage.
    
    What it does:
    1. Renders the index.html template
    2. Passes variables to the template
    3. Returns the complete HTML to the browser
    
    The variables are:
      title:     The page title (appears in browser tab)
      framework: The web framework we're using
      database:  The database we're using
    
    These get inserted into the HTML where you see {{ variable_name }}
    """

    return render_template('index.html')

    # return render_template(
    #     'index.html',                      # The HTML template file
    #     title="Job Application Tracker",   # Replaces {{ title }}
    #     framework="Flask",                 # Replaces {{ framework }}
    #     database="SQLite"                  # Replaces {{ database }}
    # )


# =============================================================================
# RUN THE APPLICATION - Start the server
# =============================================================================

# __name__ is a special Python variable
# 
# When you run this file directly with 'python app.py':
#   __name__ is set to '__main__' (True)
#   This block of code runs
# 
# When you import this file from another Python file:
#   __name__ is set to 'app' (False)
#   This block does NOT run

if __name__ == '__main__':
    
    # --- Step 1: Create the database tables ---
    # 
    # app.app_context() creates an "application context"
    # Some Flask extensions (like SQLAlchemy) need this to work properly
    # 
    # db.create_all() does:
    #   1. Checks if the database file exists
    #   2. If not, creates it
    #   3. Checks if the 'applications' table exists
    #   4. If not, creates it based on your Application model
    #   5. If it exists, leaves it alone (doesn't overwrite your data)

    with app.app_context():
        db.create_all()
    
    # --- Step 2: Start the Flask development server ---
    # 
    # app.run() starts the server that listens for incoming requests
    # 
    # debug=True:  Enables debug mode
    #   - Auto-reload: The server restarts when you change code
    #   - Debugger: Shows detailed error pages in the browser
    #   - Pin: Shows a PIN for remote debugging
    #   - Never use debug=True in production!
    # 
    # host='0.0.0.0': Makes the server accessible on your network
    #   - 127.0.0.1: Only your computer can access it
    #   - 0.0.0.0: Any device on your network can access it
    #   - This is useful for testing on your phone or other devices
    # 
    # port=5000: Runs on port 5000
    #   - Port 5000 is the default Flask port
    #   - If 5000 is in use, you can change to 5001, 8080, etc.

    app.run(
        debug=True,          # Enable debug mode (auto-reload, detailed errors)
        host='0.0.0.0',      # Allow connections from other devices on your network
        port=5000            # Use port 5000 (default Flask port)
    )