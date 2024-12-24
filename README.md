# Carputer Dashboard

The Carputer Dashboard is a web-based application designed to collect, process, and display real-time trip metrics and system status for in-vehicle use. This project is tailored for personal use, with a focus on improving functionality, robustness, and usability over time.

The application uses a Flask server running on a Raspberry Pi to serve a dashboard accessible via a browser. It integrates GPS data, system metrics, and trip-specific calculations to present critical information for monitoring and analysis during a drive. The dashboard is designed for simplicity and readability, making it suitable for use in various lighting and driving conditions.

---

## How It Works

1. **Web Server:** A Flask-based server runs on the Raspberry Pi, providing data endpoints and a user-friendly frontend.
2. **Data Collection:** Metrics are collected from GPS modules and Raspberry Pi system monitoring tools.
3. **Dashboard:** The web-based frontend displays trip-specific metrics (e.g., elapsed time, distance, speed) and system health indicators (e.g., CPU load, memory usage).
4. **User Interaction:** Buttons allow starting, stopping, and resetting trip calculations, while visual indicators provide real-time status updates.

---

## Field Reference Table

| **Field Name**         | **Description**                                                                                 | **Behavior**                                                                                     |
|------------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `Trip Status`          | Indicates the current state of the trip: "Running," or "Stopped."                               | Updates dynamically based on the trip's lifecycle.                                               |
| `Speed`                | Current speed of the vehicle (in mph) based on GPS data.                                        | Updates in real-time every second. Displays `--` if GPS data is unavailable.                     |
| `Elapsed Time`         | Total time since the trip started (HH:MM:SS format).                                            | Updates continuously while the trip is running. Resets to `--` after a trip reset.               |
| `Distance`             | Total distance covered during the trip (in miles).                                              | Calculated using the haversine formula. Resets to `0.00` after a trip reset.                     |
| `Overall Avg`          | Average speed including all time (moving and stopped) during the trip.                          | Calculated as `distance / elapsed time`. Displays `--` when the trip is inactive.                |
| `Moving Avg`           | Average speed during periods when the vehicle is moving (excluding stopped time).               | Calculated as `distance / moving time`. Displays `--` when the trip is inactive.                 |
| `Moving Time`          | Total time the vehicle has been in motion (HH:MM:SS format).                                    | Excludes time when speed is 0 mph for more than 3 seconds. Displays `--` when inactive.          |
| `Stopped Time`         | Total time the vehicle has been stationary (HH:MM:SS format).                                   | Starts counting when speed is 0 mph for more than 3 seconds. Displays `--` when inactive.        |
| `Max Speed`            | Highest speed recorded during the trip (in mph).                                                | Updates dynamically. Resets to `--` after a trip reset.                                          |
| `Projected Time`       | Estimated time to complete the trip at the current overall average speed.                       | Placeholder for future implementation. Displays `--` for now.                                    |
| `Required Speed`       | Speed required to complete the trip within a specified target time.                             | Placeholder for future implementation. Displays `--` for now.                                    |
| `CPU Load`             | Current CPU usage of the Raspberry Pi (percentage).                                             | Updates dynamically every second. Displays `--%` if data is unavailable.                         |
| `CPU Temp`             | Current temperature of the Raspberry Pi CPU (in °C).                                            | Updates dynamically every second. Displays `--°C` if data is unavailable.                        |
| `GPSD Status`          | Connection status of the GPS daemon (`Connected` or `Disconnected`).                            | Updates dynamically based on GPS availability.                                                   |
| `Satellites Locked`    | Number of satellites currently locked for GPS positioning.                                      | Updates dynamically every second. Displays `--` if no satellites are locked.                     |
| `System Uptime`        | Total time the Raspberry Pi has been running (HH:MM:SS format).                                 | Updates dynamically. Displays `--` if data is unavailable.                                       |
| `PiAware`              | Status of the PiAware service (`Running` or `Stopped`).                                         | Updates dynamically. Displays `--` if the service is not configured.                             |
| `Dump1090`             | Status of the ADS-B service for 1090 MHz (`Running` or `Stopped`).                              | Updates dynamically. Displays `--` if the service is not configured.                             |
| `Dump978`              | Status of the ADS-B service for 978 MHz (`Running` or `Stopped`).                               | Updates dynamically. Displays `--` if the service is not configured.                             |
| `Restart Carputer`     | Button to restart the Raspberry Pi.                                                             | Prompts confirmation before executing.                                                           |
| `Shutdown Carputer`    | Button to safely power off the Raspberry Pi.                                                    | Prompts confirmation before executing.                                                           |


