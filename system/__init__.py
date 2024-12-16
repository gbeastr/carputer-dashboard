# system/__init__.py
from flask import Blueprint, jsonify
import subprocess

system_bp = Blueprint('system', __name__, url_prefix="/system")

# Existing imports from system files...
from .cpu import *
from .memory import *
from .uptime import *
from .network import *
from .adsb import *

@system_bp.route('/restart', methods=['POST'])
def restart_system():
    try:
        # This command will reboot the system
        # Note: Must have appropriate permissions (e.g. sudo with no password)
        subprocess.run(["sudo", "reboot"], check=True)
        return jsonify({"status": "system is rebooting"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@system_bp.route('/shutdown', methods=['POST'])
def shutdown_system():
    try:
        # This command will power off the system
        subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
        return jsonify({"status": "system is shutting down"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

