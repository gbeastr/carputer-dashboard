# Carputer Dashboard

Flask based web app to display important status information while driving including a trip computer to track distances and average speeds.

---

## How It Works

**Web Server:** Flask-based server runs on a rpi 5, providing data endpoints that the front end calls to display data.
**Data Collection:** Metrics are collected from a u-blox gps, 2x noolec sdrs running piaware, and rpi 5 system monitoring tools like psutil.
**Dashboard:** Frontend displays trip-specific metrics (elapsed time, distance, speed, etc) and system status indicators (CPU load, temp, uptime, etc)
**User Interaction:** Buttons on the frontend to start, stop, and reset the trip calculations, while visual indicators provide real-time status updates.

---

## Trip Computer

Flask opens a gps thread with gpsd and polls for necessary fields and returns them to an endpoint <ip>:<port>/trip/gps.

The json response looks like:

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

Metrics.py then interprets this data and calculates all necessary fields when the user starts the trip.

---

## Status Metrics/Other Info

All other data the pi collects is collected by scripts under /system. Most are very straighforward, such as cpu.py and network.py (use psutil to get cpu and network health).

bluetooth.py: this module only shows if the pi is connected to the android tablet running bluetooth or not. It does not try to reconnect on disconnect or start tethering. Still planning on adding this functionality.

weather.py: this module calls https://api.openweathermap.org/data/2.5/weather for temperature in fahrenheit every 5 minutes. With this interval api calls will always be free.






    
