from flask import jsonify
import psutil
from . import system_bp

@system_bp.route('/system/memory', methods=['GET'])
def memory_metrics():
    metrics = {
        "memory_usage": psutil.virtual_memory().percent
    }
    return jsonify(metrics)

