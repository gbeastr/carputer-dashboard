# network.py
from flask import jsonify
import psutil
import os
import socket
import subprocess
from . import system_bp

def get_interface_status(interface_name):
    """
    Get the status and IP address of a specific network interface.
    """
    stats = psutil.net_if_stats().get(interface_name, None)
    if not stats or not stats.isup:
        return {"status": "down", "ip_address": None}

    addrs = psutil.net_if_addrs().get(interface_name, [])
    ip_address = next(
        (addr.address for addr in addrs if addr.family == socket.AF_INET),
        None
    )
    return {"status": "up", "ip_address": ip_address}

def get_wifi_ssid():
    """
    Get the SSID of the connected WiFi network, if any.
    """
    try:
        ssid = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
        return ssid if ssid else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def check_router_connectivity(router_ip="192.168.1.1"):
    """
    Check connectivity to the local router by pinging its IP.
    """
    response = os.system(f"ping -c 1 -W 1 {router_ip} > /dev/null 2>&1")
    return "OK" if response == 0 else "Failed"

def has_internet():
    """
    Ping google.com (or 8.8.8.8) once with a 1s timeout to see if we have internet connectivity.
    """
    response = os.system("ping -c 1 -W 1 google.com > /dev/null 2>&1")
    return (response == 0)

@system_bp.route('/network', methods=['GET'])
def network_metrics():
    """
    Endpoint to return network status for Ethernet and WiFi, 
    plus router connectivity and internet availability.
    """
    # Check Ethernet
    ethernet = get_interface_status("eth0")  # Update if your Ethernet interface name differs
    # Check WiFi
    wifi = get_interface_status("wlan0")     # Update if your WiFi interface name differs
    wifi["ssid"] = get_wifi_ssid()          # Attempt to get the SSID if present

    # Check local router connectivity
    router_status = check_router_connectivity("192.168.1.1")  # Adjust IP if needed

    # Check internet
    internet_ok = has_internet()

    return jsonify({
        "ethernet": ethernet,
        "wifi": wifi,
        "connection_to_router": router_status,
        "internet": "OK" if internet_ok else "Failed"
    })

