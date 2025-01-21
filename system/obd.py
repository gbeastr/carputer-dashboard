from flask import jsonify
import obd
from . import system_bp

# Attempt to connect to the OBD-II adapter
connection = obd.OBD("/dev/rfcomm0")  # Update with the correct port if necessary

# Helper function to fetch OBD data safely
def fetch_obd_data(command):
    if connection.is_connected():
        response = connection.query(command)
        return response.value if response and response.is_successful() else None
    return None

@system_bp.route('/obd', methods=['GET'])
def obd_metrics():
    # Define the important OBD metrics to fetch
    data = {
        "speed": fetch_obd_data(obd.commands.SPEED),  # Vehicle speed
        "rpm": fetch_obd_data(obd.commands.RPM),  # Engine RPM
        "fuel_level": fetch_obd_data(obd.commands.FUEL_LEVEL),  # Fuel level percentage
        "coolant_temp": fetch_obd_data(obd.commands.COOLANT_TEMP),  # Coolant temperature
        "throttle_position": fetch_obd_data(obd.commands.THROTTLE_POS),  # Throttle position
        "engine_load": fetch_obd_data(obd.commands.ENGINE_LOAD),  # Engine load percentage
        "voltage": fetch_obd_data(obd.commands.CONTROL_MODULE_VOLTAGE),  # Control module voltage
    }
    return jsonify(data)

