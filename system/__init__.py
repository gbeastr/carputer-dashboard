# system/__init__.py

from flask import Blueprint, jsonify
import subprocess

# Create the main "system" blueprint
system_bp = Blueprint("system", __name__, url_prefix="/system")

# Import submodules that attach routes directly to system_bp
from .cpu import *
from .memory import *
from .uptime import *
from .network import *
from .adsb import *
from .weather import *
from .bluetooth import *

@system_bp.route('/restart', methods=['POST'])
def restart_system():
    """
    Reboot the system. Requires sudo permission with no password (visudo).
    """
    try:
        subprocess.run(["sudo", "reboot"], check=True)
        return jsonify({"status": "system is rebooting"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@system_bp.route('/shutdown', methods=['POST'])
def shutdown_system():
    """
    Power off the system. Also requires sudo permission with no password.
    """
    try:
        subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
        return jsonify({"status": "system is shutting down"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

