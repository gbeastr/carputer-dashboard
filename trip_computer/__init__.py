from flask import Blueprint

# Define the trip_computer blueprint
trip_bp = Blueprint('trip', __name__, url_prefix="/trip")

# Import routes and functions
from .gps import *
