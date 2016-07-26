from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create flask app
app = Flask(__name__)

# Load the default configuration
app.config.from_object('config.DefaultConfig')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from app.automatization.scheduler_manager import start_scheduler
from app import public
from app import admin

# Start scheduler with automatic importation
start_scheduler()
