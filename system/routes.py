from flask import jsonify
import psutil
from . import system_bp

@system_bp.route('/system', methods=['GET'])
def system_metrics():
    # Get CPU and memory usage
    metrics = {
        "cpu_load": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent
    }
    return jsonify(metrics)

