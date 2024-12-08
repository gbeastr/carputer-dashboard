from flask import Blueprint

# define the system blueprint
system_bp = Blueprint('system', __name__, url_prefix="/system")

# import routes from individual modules
from .cpu import *
from .memory import *
from .uptime import *
from .network import *
from .adsb import *

