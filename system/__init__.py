from flask import Blueprint

# Define the Blueprint
system_bp = Blueprint('system', __name__)

# Import the routes (we'll create them next)
from .routes import *

