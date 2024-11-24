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
    # Create a gpsd session
    session = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    while True:
        try:
            # Wait for the next report from the GPS daemon.
            report = session.next()

            # Handle TPV (Time-Position-Velocity) reports
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
                else:
                    gps_data["status"] = "no fix"

            # Handle SKY reports to get satellite information
            elif report['class'] == 'SKY':
                gps_data["satellites_used"] = report.get('uSat', 0)

        except KeyError:
            # Handle missing data in the report
            continue
        except StopIteration:
            # GPSD has terminated
            print("GPSD has terminated")
            break
        except Exception as e:
            print(f"Error in GPS polling thread: {e}")
            break

# Start the GPS polling thread
gps_thread = threading.Thread(target=gps_polling, daemon=True)
gps_thread.start()

@trip_bp.route('/gps', methods=['GET'])
def gps_metrics():
    """
    GPS endpoint to fetch real-time GPS data.
    """
    # Prepare a copy of the GPS data to avoid threading issues
    output_data = gps_data.copy()

    # Convert speed from m/s to mph if available
    speed = output_data.get('speed', 'N/A')
    if isinstance(speed, (int, float)):
        output_data['speed'] = speed * 2.237  # Convert m/s to mph
    else:
        output_data['speed'] = 'N/A'

    # Format the data for JSON response
    return jsonify(output_data)

