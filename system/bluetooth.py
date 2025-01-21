# bluetooth.py
import subprocess
from flask import jsonify
from . import system_bp

# Replace this MAC address with the device you’re interested in
TARGET_MAC = "C4:7D:9F:C0:AB:D2"

def is_bt_connected(mac=TARGET_MAC) -> bool:
    """
    Checks if the given MAC is currently in the output of 'hcitool con'.
    If so, we assume a Bluetooth connection is active.
    """
    try:
        output = subprocess.check_output(["hcitool", "con"], text=True)
        # Look for the MAC in the connection list
        return mac.upper() in output.upper()
    except Exception as e:
        # If hcitool isn't installed or something else goes wrong,
        # treat it as not connected
        print(f"Error checking Bluetooth connection: {e}")
        return False

@system_bp.route('/bluetooth', methods=['GET'])
def bluetooth_status():
    """
    Endpoint: GET /system/bluetooth
    Returns JSON like:
      {
        "device_mac": "C4:7D:9F:C0:AB:D2",
        "connected": true/false
      }
    """
    connected = is_bt_connected(TARGET_MAC)
    return jsonify({
        "device_mac": TARGET_MAC,
        "connected": connected
    })

