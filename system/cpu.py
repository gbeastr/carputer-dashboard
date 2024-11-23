from flask import jsonify
import psutil
from . import system_bp

@system_bp.route('/system/cpu', methods=['GET'])
def cpu_metrics():
    cpu_load = psutil.cpu_percent(interval=0)
    temperatures = psutil.sensors_temperatures()

    # Safely get the CPU temperature
    cpu_temp = 'N/A'
    if 'cpu_thermal' in temperatures:
        cpu_temp = temperatures['cpu_thermal'][0].current

    metrics = {
        "cpu_load": cpu_load,
        "cpu_temperature": cpu_temp
    }
    return jsonify(metrics)

