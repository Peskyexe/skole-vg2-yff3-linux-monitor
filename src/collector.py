# source .venv/bin/activate

import socket
import subprocess
import json
import time
from datetime import datetime
import re

try: 
    import psutil
except ModuleNotFoundError:
    print("[!] Virtual environment might not be activated. Run command: 'source .venv/bin/activate' to activate it.")
    quit()  


# In seconds
UPDATE_FREQUENCY = 2


def bytes_to_gb(bytes):
    return round(bytes / (1024**3), 1)


def get_cpu_dict():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    
    temps = psutil.sensors_temperatures()
    package_temp = temps['coretemp'][0][1]
    
    return {
        "cpu_current_freq": round(cpu_freq.current),
        "cpu_package_temp": package_temp,
        "cpu_used_percent": round(cpu_percent)
    }


def get_memory_dict():
    memory = psutil.virtual_memory()
    return {
        "memory_total_gb": bytes_to_gb(memory.total),
        "memory_free_gb": bytes_to_gb(memory.available),
        "memory_used_gb": bytes_to_gb(memory.used),
        "memory_used_percent": round(memory.percent)
    }


def get_disk_dict():
    disk = psutil.disk_usage('/')
    return {
        "disk_total_gb": bytes_to_gb(disk.total),
        "disk_free_gb": bytes_to_gb(disk.free),
        "disk_used_gb": bytes_to_gb(disk.used),
        "disk_used_percent": round(disk.percent)
    }


# Generel system info
def get_system_info_dict():
    # Bruker Regex til å hente ut OS og kernel fra 'hostnamectl' kommandoen.
    system_summary_result = subprocess.run(["hostnamectl"], capture_output=True, text=True)

    os = re.search(r"Operating System:\s*(.+)$", system_summary_result.stdout, flags=re.MULTILINE).group(1)
    kernel = re.search(r"Kernel:\s*(.+)$", system_summary_result.stdout, flags=re.MULTILINE).group(1)
    
    # Henter IP-en med 'ip addr' kommanoden og Regex.
    ip_addr_result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
    ip_addr = ip_addr_result.stdout.strip()
    
    if ip_addr == '':
        ip_addr = 'No connection'
    
    def get_uptime():
        # Henter boot tid i sekunder siden epoken (Unix epoch)
        boot_timestamp = round(psutil.boot_time())
        
        boot_time = datetime.fromtimestamp(boot_timestamp)
        current_time = datetime.now()
        
        # uptime er et TimeDelta objekt 
        uptime = current_time - boot_time
        
        # Formaterer uptime TimeDelta objektet til en string
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days} days, {hours} hours, {minutes} minutes"
    
    return {
        "hostname": socket.gethostname(),
        "os": os,
        "kernel": kernel,
        "ip_addr": ip_addr,
        "uptime": get_uptime(),
        "process_count": len(psutil.pids())
    }


def get_system_data():
    system_data = {
        "system_info": get_system_info_dict(),
        "cpu": get_cpu_dict(),
        "memory": get_memory_dict(),
        "disk": get_disk_dict()
    }
    
    return system_data


def save_system_data(system_data):
    try:
        with open("shared/systemdata.json", "w") as file:
            json.dump(system_data, file, indent=4)
            
    except TypeError as e:
        print(f"JSON serialization error: {e}")
        
    except OSError as e:
        print(f"File I/O error: {e}")


def update_system_state():
    current_system_data = get_system_data()
    save_system_data(current_system_data)


if __name__ == "__main__":
    system_data = get_system_data()
    print(f"Host machine IP address: {system_data['system_info']['ip_addr']}")
    
    while True:
        update_system_state()
        time.sleep(UPDATE_FREQUENCY)
