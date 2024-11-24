from flask import Blueprint

# Define the system blueprint
system_bp = Blueprint('system', __name__, url_prefix="/system")

# Import routes from individual modules
from .cpu import *
from .memory import *
from .uptime import *
from .network import *
from .gps import *
