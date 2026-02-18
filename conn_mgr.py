import json
import logging
import time

# 1. Setup Logging for errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='network_ops.log'
)

class DeviceConnector:
    def __init__(self, ip, hostname):
        self.ip = ip
        self.hostname = hostname

    def connect_to_device(self, simulate_failure=False):
        """Simulates a Netmiko connection with error handling."""
        print(f"Attempting connection to {self.hostname} ({self.ip})...")
        logging.info(f"Connecting to {self.ip}")
        
        try:
            # Simulate network latency
            time.sleep(1) 
            
            if simulate_failure:
                # This mimics a Netmiko Timeout or Auth Failure
                raise ConnectionError(f"Timeout: Device {self.ip} unreachable.")
            
            print(f"Success! Connected to {self.hostname}.")
            logging.info(f"Successfully authenticated to {self.hostname}")
            return True

        except ConnectionError as e:
            logging.error(f"Failed to connect to {self.ip}: {e}")
            print(f"ERROR: Could not connect. Check 'network_ops.log' for details.")
            return False

# --- Removed hardcoded fake devices inventory and input a json inventory file---
if __name__ == "__main__":
    # Create a test list of "Devices"
    # input a json inventory file"

    '''inventory = [
        {"ip": "10.1.1.1", "name": "Core_Switch_01", "fail": False},
        {"ip": "10.1.1.5", "name": "Branch_Router_02", "fail": True} # This one will fail
    ]
    for dev in inventory:
        conn = DeviceConnector(dev['ip'], dev['name'])
        conn.connect_to_device(simulate_failure=dev['fail'])'''

    # input a json inventory file"
    try:
        with open("inventory.json", "r") as f:
            devices = json.loads(f)

        for dev in devices:
            conn = DevicConnector(dev['ip'], dev['name'])
            conn.connect_to_device(simulate_failure=dev['failstatus'])

    except FileNotFoundError:
            print("Error! inventory.json file not found!")
    except PermissionError:
            print("Error! inventory.json file lacks necessary permissions!")
    except json.JSONDecodeError:
            print("Error! inventory.json file has malformed syntax and/or invalid values!")
    except IOError:
            print("FileI/O or OS related errors!")
