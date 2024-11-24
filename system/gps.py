from flask import jsonify
import subprocess
import json
from . import system_bp  # Import system_bp for route registration

def get_gps_data():
    """
    Fetch GPS data using gpspipe and return relevant metrics.
    """
    try:
        # Fetch a single batch of JSON data from gpspipe
        process = subprocess.run(
            ["gpspipe", "-w", "-n", "5"], capture_output=True, text=True, timeout=2
        )

        # Initialize GPS data structure
        gps_data = {
            "status": "not connected",
            "satellites_used": None,
            "latitude": None,
            "longitude": None,
            "altitude": None,
            "speed": None,
            "horizontal_accuracy": None,
            "heading": None,
            "timestamp": None
        }

        # Process each line of gpspipe output
        for line in process.stdout.splitlines():
            try:
                data = json.loads(line)

                # Extract TPV data for position and movement
                if data.get("class") == "TPV":
                    gps_data["latitude"] = data.get("lat")
                    gps_data["longitude"] = data.get("lon")
                    gps_data["altitude"] = data.get("alt")
                    gps_data["speed"] = data.get("speed")
                    gps_data["horizontal_accuracy"] = data.get("epx")
                    gps_data["heading"] = data.get("track")
                    gps_data["timestamp"] = data.get("time")
                    gps_data["status"] = "connected"

                # Extract SKY data for satellites used
                if data.get("class") == "SKY":
                    gps_data["satellites_used"] = data.get("uSat", None)

                # Break early if both TPV and SKY data are populated
                if gps_data["status"] == "connected" and gps_data["satellites_used"] is not None:
                    break
            except json.JSONDecodeError:
                continue  # Skip invalid JSON lines

        return gps_data

    except subprocess.TimeoutExpired:
        return {"error": "Timeout while reading GPS data"}
    except Exception as e:
        return {"error": str(e)}

@system_bp.route('/gps', methods=['GET'])
def gps_metrics():
    """
    GPS endpoint to fetch real-time GPS data.
    """
    data = get_gps_data()
    return jsonify(data)

