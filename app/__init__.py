from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

# Create flask app
app = Flask(__name__)

# Load the default configuration
app.config.from_object('config.DefaultConfig')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from . import public
from . import admin