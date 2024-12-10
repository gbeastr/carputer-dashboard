import os
import csv
import time
import math
from flask import jsonify
from datetime import datetime
from threading import Thread
from . import trip_bp
from .gps import gps_data

# Trip Data
trip_data = {
    "start_time": None,
    "elapsed_time": 0,
    "distance_covered": 0.0,
    "running": False,
    "stopped_time": 0.0,
    "moving_average_speed": 0.0,
    "last_update_time": None,
    "last_lat": None,
    "last_lon": None,
    "cumulative_speed": 0.0,
    "speed_count": 0,
    "max_speed": 0.0
}

# Logging Globals
LOG_DIR = "/home/gheyman/carputer/trip_logs"
trip_log_file = None
logging_active = False

# Haversine Function
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Radius of Earth in miles
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Logger Functions
def get_next_trip_file():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)  # Create log directory if it doesn't exist
    existing_files = sorted([f for f in os.listdir(LOG_DIR) if f.startswith("trip_") and f.endswith(".csv")])
    if existing_files:
        last_file = existing_files[-1]
        last_number = int(last_file.split("_")[1].split(".")[0])
        next_number = last_number + 1
    else:
        next_number = 1
    return f"{LOG_DIR}/trip_{str(next_number).zfill(3)}.csv"

def initialize_trip_logger():
    global trip_log_file
    trip_log_file = get_next_trip_file()
    with open(trip_log_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Elapsed", "Latitude", "Longitude", "Speed (mi)", "Distance (mi)"])  # Header

def log_trip_metrics():
    try:
        lat = gps_data.get("latitude", "N/A")
        lon = gps_data.get("longitude", "N/A")
        speed = gps_data.get("speed", 0)
        elapsed = trip_data.get("elapsed_time", 0)
        elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        if trip_data["last_lat"] is not None and trip_data["last_lon"] is not None:
            trip_data["distance_covered"] += haversine(trip_data["last_lat"], trip_data["last_lon"], lat, lon)

        with open(trip_log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                elapsed_str,
                lat,
                lon,
                round(speed * 2.237, 1) if isinstance(speed, (int, float)) else "N/A",
                round(trip_data["distance_covered"], 2)
            ])
    except Exception as e:
        print(f"Error logging trip metrics: {e}")

def start_logging():
    global logging_active
    initialize_trip_logger()
    logging_active = True
    Thread(target=log_trip_loop, daemon=True).start()

def stop_logging():
    global logging_active
    logging_active = False

def log_trip_loop():
    while logging_active:
        log_trip_metrics()
        time.sleep(1)

# Trip Endpoints
@trip_bp.route('/start', methods=['POST'])
def start_trip():
    if trip_data["running"]:
        return jsonify({"status": "trip already running"}), 400
    if trip_data["elapsed_time"] > 0 or trip_data["distance_covered"] > 0:
        return jsonify({"status": "please reset trip before starting a new one"}), 400

    current_time = time.time()
    trip_data.update({
        "start_time": current_time,
        "elapsed_time": 0,
        "distance_covered": 0.0,
        "running": True,
        "stopped_time": 0.0,
        "moving_average_speed": 0.0,
        "cumulative_speed": 0.0,
        "speed_count": 0,
        "last_update_time": current_time,
        "last_lat": None,
        "last_lon": None,
        "max_speed": 0.0
    })

    start_logging()  # Start logging when trip starts
    return jsonify({"status": "trip started"})

@trip_bp.route('/stop', methods=['POST'])
def stop_trip():
    if not trip_data["running"]:
        return jsonify({"status": "trip is not running"}), 400
    current_time = time.time()
    trip_data["elapsed_time"] = current_time - trip_data["start_time"]
    trip_data["running"] = False

    stop_logging()  # Stop logging when trip stops
    return jsonify({"status": "trip stopped"})

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
        "cumulative_speed": 0.0,
        "speed_count": 0,
        "last_update_time": None,
        "last_lat": None,
        "last_lon": None,
        "max_speed": 0.0
    })
    return jsonify({"status": "trip reset"})

@trip_bp.route('/metrics', methods=['GET'])
def get_metrics():
    if trip_data["running"]:
        current_time = time.time()
        delta = current_time - trip_data["last_update_time"] if trip_data["last_update_time"] else 0
        trip_data["elapsed_time"] = current_time - trip_data["start_time"]

        lat = gps_data.get("latitude", None)
        lon = gps_data.get("longitude", None)
        speed_mph = gps_data.get("speed", 0)

        # Update distance covered if speed > 0
        if (trip_data["last_lat"] is not None and trip_data["last_lon"] is not None and
            isinstance(lat, (float, int)) and isinstance(lon, (float, int))):
            dist = haversine(trip_data["last_lat"], trip_data["last_lon"], lat, lon)
            if speed_mph > 0.1:
                trip_data["distance_covered"] += dist

        # Update moving average speed and max speed
        if speed_mph > 0.1:
            trip_data["cumulative_speed"] += speed_mph
            trip_data["speed_count"] += 1
            trip_data["moving_average_speed"] = trip_data["cumulative_speed"] / trip_data["speed_count"]
            trip_data["max_speed"] = max(trip_data["max_speed"], speed_mph)
        else:
            trip_data["stopped_time"] += delta

        # Update last known location and time
        trip_data.update({
            "last_lat": lat,
            "last_lon": lon,
            "last_update_time": current_time
        })

    overall_average_speed = (
        trip_data["distance_covered"] / (trip_data["elapsed_time"] / 3600)
        if trip_data["elapsed_time"] > 0 else 0
    )
    moving_time = max(0, trip_data["elapsed_time"] - trip_data["stopped_time"])

    return jsonify({
        "running": trip_data["running"],
        "elapsed_time": trip_data["elapsed_time"],
        "distance_covered": trip_data["distance_covered"],
        "stopped_time": trip_data["stopped_time"],
        "moving_average_speed": trip_data["moving_average_speed"],
        "overall_average_speed": overall_average_speed,
        "moving_time": moving_time,
        "max_speed": trip_data["max_speed"]
    })

