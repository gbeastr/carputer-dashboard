from flask import jsonify
import time
from . import system_bp

@system_bp.route('/uptime', methods=['GET'])
def uptime_metrics():
    boot_time = time.time() - time.monotonic()
    uptime_seconds = time.monotonic()

    metrics = {
        "boot_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(boot_time)),
        "uptime_seconds": int(uptime_seconds)
    }
    return jsonify(metrics)

