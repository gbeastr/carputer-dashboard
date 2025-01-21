import requests
from flask import jsonify
from . import system_bp
from trip_computer.gps import gps_data

API_KEY = "8476fda10939d0b280e3ed06340e89db"  # Hard-code your key here
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@system_bp.route('/weather', methods=['GET'])
def get_weather():
    lat = gps_data.get("latitude", None)
    lon = gps_data.get("longitude", None)

    # If no valid GPS fix, bail out
    if not isinstance(lat, (float, int)) or not isinstance(lon, (float, int)):
        return jsonify({"outside_temp_f": None, "error": "GPS fix not available"}), 400

    # Make the request to OpenWeatherMap (Free tier)
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "imperial"
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=5)
        data = resp.json()

        # The current temp is under data["main"]["temp"]
        current_temp_f = data["main"]["temp"]
        return jsonify({"outside_temp_f": current_temp_f})

    except requests.exceptions.RequestException as e:
        return jsonify({"outside_temp_f": None, "error": f"Request error: {e}"}), 500
    except KeyError:
        # If the JSON doesn't have "main"/"temp", you'll end up here
        return jsonify({"outside_temp_f": None, "error": "Unexpected response structure"}), 500

