# gps.py

import gps
import threading
from flask import jsonify
from . import trip_bp

# Shared GPS data dictionary
gps_data = {
    "status": "no fix",
    "satellites_used": 0,
    "latitude": 'N/A',
    "longitude": 'N/A',
    "altitude": 'N/A',
    "speed": 'N/A',
    "horizontal_accuracy": 'N/A',
    "heading": 'N/A',
    "timestamp": 'N/A'
}

def gps_polling():
    """
    Background thread function to continuously read GPS data.
    """
    session = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    while True:
        try:
            report = session.next()

            if report['class'] == 'TPV':
                if getattr(report, 'mode', 1) >= 2:
                    gps_data["status"] = "connected"
                    gps_data["latitude"] = getattr(report, 'lat', 'N/A')
                    gps_data["longitude"] = getattr(report, 'lon', 'N/A')
                    gps_data["altitude"] = getattr(report, 'alt', 'N/A')
                    gps_data["speed"] = getattr(report, 'speed', 'N/A')
                    gps_data["heading"] = getattr(report, 'track', 'N/A')
                    gps_data["timestamp"] = getattr(report, 'time', 'N/A')
                    gps_data["horizontal_accuracy"] = getattr(report, 'epx', 'N/A')

                    # Convert speed from m/s to mph if it's numeric
                    if isinstance(gps_data["speed"], (int, float)):
                        gps_data["speed"] = gps_data["speed"] * 2.237
                else:
                    gps_data["status"] = "no fix"

            elif report['class'] == 'SKY':
                gps_data["satellites_used"] = report.get('uSat', 0)

        except KeyError:
            continue
        except StopIteration:
            print("GPSD has terminated")
            break
        except Exception as e:
            print(f"Error in GPS polling thread: {e}")
            break

gps_thread = threading.Thread(target=gps_polling, daemon=True)
gps_thread.start()

@trip_bp.route('/gps', methods=['GET'])
def gps_metrics():
    """
    GPS endpoint to fetch real-time GPS data, already in MPH.
    """
    output_data = gps_data.copy()
    # gps_data now already stores speed in MPH, so no need to re-convert here.
    return jsonify(output_data)

