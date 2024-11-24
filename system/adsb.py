from flask import jsonify
import subprocess
import threading
from . import system_bp

# Map of service names to their actual systemd unit names
ADS_B_SERVICES = {
    "piaware": "piaware",
    "dump1090": "dump1090-fa",  # Corrected service name
    "dump978": "dump978-fa"     # Corrected service name
}

def check_service_status(service_name):
    """
    Check the status of a service using systemctl.
    Returns:
        - "running" if the service is active.
        - "stopped" if the service is inactive.
        - "not found" if the service does not exist.
        - "error" if an unexpected status occurs.
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
    Restart a service using systemctl with sudo.
    Returns:
        - "restart successful" if the restart succeeds.
        - "restart failed" if the restart fails.
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
    Background thread to restart services that are stopped or in error state.
    """
    for service, status in services.items():
        if status in ["stopped", "error"]:
            print(f"{service} is {status}. Attempting restart...")
            restart_result = restart_service(ADS_B_SERVICES[service])
            print(f"Restart result for {service}: {restart_result}")

@system_bp.route('/adsb', methods=['GET'])
def adsb_metrics():
    """
    Endpoint to return the status of ADS-B related services.
    If a service is stopped or in error, a background thread attempts to restart it.
    """
    # Check the status of all services
    services = {
        service: check_service_status(systemd_name)
        for service, systemd_name in ADS_B_SERVICES.items()
    }

    # Start a background thread to restart any failed services
    thread = threading.Thread(target=restart_failed_services, args=(services,))
    thread.start()

    # Return the current status immediately
    return jsonify(services)

