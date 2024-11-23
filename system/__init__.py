from flask import Blueprint

# Define the Blueprint
system_bp = Blueprint('system', __name__)

# Import routes
from .cpu import *
from .memory import *
from .uptime import *

