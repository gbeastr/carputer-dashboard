from flask import jsonify
import psutil
import subprocess
import os
import socket
from . import system_bp

def get_interface_status(interface_name):
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
    try:
        ssid = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
        return ssid if ssid else None
    except subprocess.CalledProcessError:
        return None

def check_router_connectivity(router_ip="192.168.1.1"):
    response = os.system(f"ping -c 1 -W 1 {router_ip} > /dev/null 2>&1")
    return "OK" if response == 0 else "Failed"

@system_bp.route('/system/network', methods=['GET'])
def network_metrics():
    ethernet = get_interface_status("eth0")
    wifi = get_interface_status("wlan0")
    wifi["ssid"] = get_wifi_ssid()
    router_status = check_router_connectivity()

    return jsonify({
        "ethernet": ethernet,
        "wifi": wifi,
        "connection_to_router": router_status
    })

