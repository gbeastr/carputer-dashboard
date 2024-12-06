import time
from flask import jsonify
from . import trip_bp

# Trip data to track
trip_data = {
    "start_time": None,       # When the trip started
    "elapsed_time": 0,        # Total time for the trip (seconds)
    "distance_covered": 0.0,  # Distance covered (miles)
    "running": False,         # Whether the trip is currently running
    "stopped_time": 0.0,      # Total time spent stopped (seconds)
    "moving_average_speed": 0.0, # Average speed while moving (mph)
}

# Start the trip
@trip_bp.route('/start', methods=['POST'])
def start_trip():
    if trip_data["running"]:
        return jsonify({"status": "trip already running"}), 400
    if trip_data["elapsed_time"] > 0 or trip_data["distance_covered"] > 0:
        return jsonify({"status": "please reset trip before starting a new one"}), 400
    trip_data["start_time"] = time.time() - trip_data["elapsed_time"]
    trip_data["running"] = True
    return jsonify({"status": "trip started"})

# Stop the trip
@trip_bp.route('/stop', methods=['POST'])
def stop_trip():
    if not trip_data["running"]:
        return jsonify({"status": "trip is not running"}), 400
    trip_data["elapsed_time"] = time.time() - trip_data["start_time"]
    trip_data["running"] = False
    return jsonify({"status": "trip stopped"})

# Reset the trip
@trip_bp.route('/reset', methods=['POST'])
def reset_trip():
    if trip_data["running"]:
        return jsonify({"status": "cannot reset while trip is running"}), 400
    trip_data.update({
        "start_time": None,
        "elapsed_time": 0,
        "distance_covered": 0.0,
        "running": False,
        "stopped_time": 0.0,
        "moving_average_speed": 0.0,
    })
    return jsonify({"status": "trip reset"})

# Get trip metrics
@trip_bp.route('/metrics', methods=['GET'])
def get_metrics():
    # Return the current state of trip data
    return jsonify(trip_data)
