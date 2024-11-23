from flask import jsonify
import psutil
import time
from datetime import datetime
from . import system_bp

@system_bp.route('/system/uptime', methods=['GET'])
def uptime_metrics():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    metrics = {
        "boot_time": datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S'),
        "uptime_seconds": int(uptime_seconds)
    }
    return jsonify(metrics)

