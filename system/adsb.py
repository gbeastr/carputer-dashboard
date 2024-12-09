from flask import jsonify
import subprocess
import threading
from . import system_bp

ADS_B_SERVICES = {
    "piaware": "piaware",
    "dump1090": "dump1090-fa",
    "dump978": "dump978-fa"
}

def check_service_status(service_name):
    """
    checks the status of a service using systemctl.
    returns:
        "running" if service is active
        "stopped" if service is inactive
        "not found" if service DNE (jerry core)
        "error" for an unexpected state
    """
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return "running"
        elif result.returncode == 3:
            return "stopped"
        else:
            return "error"
    except FileNotFoundError:
        return "not found"

def restart_service(service_name):
    """
    restarts a failed/stopped service using systemctl with sudo
    returns:
        "restart successful" if service is running
        "restart failed" if service is still stopped
    """
    print(f"Attempting to restart service: {service_name}")
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "restart", service_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"{service_name} restarted successfully.")
            return "restart successful"
        else:
            print(f"Error restarting {service_name}: {result.stderr}")
            return "restart failed"
    except Exception as e:
        print(f"Exception restarting {service_name}: {e}")
        return "restart failed"

def restart_failed_services(services):
    """
    background thread to restart services that are stopped or in error state
    """
    for service, status in services.items():
        if status in ["stopped", "error"]:
            print(f"{service} is {status}. Attempting restart...")
            restart_result = restart_service(ADS_B_SERVICES[service])
            print(f"Restart result for {service}: {restart_result}")

@system_bp.route('/adsb', methods=['GET'])
def adsb_metrics():
    """
    defines endpoint to return the status of ads-b related services.
    """
    # checks the status of all services
    services = {
        service: check_service_status(systemd_name)
        for service, systemd_name in ADS_B_SERVICES.items()
    }

    # background thread to restart failed/stopped services
    thread = threading.Thread(target=restart_failed_services, args=(services,))
    thread.start()

    # returns current service statuses
    return jsonify(services)

