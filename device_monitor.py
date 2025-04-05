# utils/device_monitor.py
import psutil

def suggest_device():
    cpu = psutil.cpu_percent()
    gpu = psutil.sensors_temperatures().get('amdgpu', [{'current': 0}])[0]['current'] if 'amdgpu' in psutil.sensors_temperatures() else 0

    if cpu > 85:
        return 'GPU'
    elif gpu > 80:
        return 'CPU'
    else:
        return 'AUTO'
