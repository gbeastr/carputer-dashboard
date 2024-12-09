import time
import math
from flask import jsonify
from . import trip_bp
from .gps import gps_data

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

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8 # radius of the earth :p
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat/2)**2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(dLon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@trip_bp.route('/start', methods=['POST'])
def start_trip():
    if trip_data["running"]:
        return jsonify({"status": "trip already running"}), 400
    if trip_data["elapsed_time"] > 0 or trip_data["distance_covered"] > 0:
        return jsonify({"status": "reset trip before starting a new one"}), 400

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
    return jsonify({"status": "trip started"})

@trip_bp.route('/stop', methods=['POST'])
def stop_trip():
    if not trip_data["running"]:
        return jsonify({"status": "trip is not running"}), 400
    current_time = time.time()
    trip_data["elapsed_time"] = current_time - trip_data["start_time"]
    trip_data["running"] = False
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
        "last_update_time": None,
        "last_lat": None,
        "last_lon": None,
        "cumulative_speed": 0.0,
        "speed_count": 0,
        "max_speed": 0.0
    })
    return jsonify({"status": "trip reset"})

@trip_bp.route('/metrics', methods=['GET'])
def get_metrics():
    if trip_data["running"]:
        current_time = time.time()
        delta = 0
        if trip_data["last_update_time"] is not None:
            delta = current_time - trip_data["last_update_time"]
        trip_data["elapsed_time"] = current_time - trip_data["start_time"]

        lat = gps_data.get("latitude", None)
        lon = gps_data.get("longitude", None)
        speed_mph = gps_data.get("speed", 0)

        # update distance covered if speed > 0
        if (trip_data["last_lat"] is not None and
            trip_data["last_lon"] is not None and
            isinstance(lat, (float, int)) and
            isinstance(lon, (float, int))):
            dist = haversine(trip_data["last_lat"], trip_data["last_lon"], lat, lon)
            if speed_mph > 0.1:
                trip_data["distance_covered"] += dist

        # update moving average speed and max speed
        if speed_mph > 0.1:
            trip_data["cumulative_speed"] += speed_mph
            trip_data["speed_count"] += 1
            if trip_data["speed_count"] > 0:
                trip_data["moving_average_speed"] = trip_data["cumulative_speed"] / trip_data["speed_count"]

            # check for new max speed
            if isinstance(speed_mph, (int, float)) and speed_mph > trip_data["max_speed"]:
                trip_data["max_speed"] = speed_mph
        else:
            # if not moving, update stopped_time
            trip_data["stopped_time"] += delta

        # update last known location and time
        if isinstance(lat, (float, int)) and isinstance(lon, (float, int)):
            trip_data["last_lat"] = lat
            trip_data["last_lon"] = lon
        trip_data["last_update_time"] = current_time

    # calculate overall average speed
    overall_average_speed = 0
    if trip_data["elapsed_time"] > 0:
        hours = trip_data["elapsed_time"] / 3600
        if hours > 0:
            overall_average_speed = trip_data["distance_covered"] / hours

    # calculate moving_time
    moving_time = trip_data["elapsed_time"] - trip_data["stopped_time"]
    if moving_time < 0:
        moving_time = 0.0

    response = {
        "running": trip_data["running"],
        "elapsed_time": trip_data["elapsed_time"],
        "distance_covered": trip_data["distance_covered"],
        "stopped_time": trip_data["stopped_time"],
        "moving_average_speed": trip_data["moving_average_speed"],
        "overall_average_speed": overall_average_speed,
        "moving_time": moving_time,
        "max_speed": trip_data["max_speed"]
    }

    return jsonify(response)

