from flask import Flask, request
import requests
import sys
import socket
import psutil
import time
import threading


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
# Update this variable as per your setup
# COUNTER_SERVICE_URL = 'http://192.168.2.2:8080' if len(sys.argv) == 1 else sys.argv[1]

app = Flask(__name__)

def cpu_load(duration_seconds):
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        # Perform CPU-intensive task
        x = 1
        for i in range(1, 100000):
            x += 1

def memory_load(memory_size_mb,duration_seconds):
    # Allocate memory
    memory_alloc = bytearray(memory_size_mb * 1024 * 1024)
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        pass
        # Continue to hold allocated memory

def network_load( duration_seconds):
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        # Send HTTP request to the specified URL
        try:
            response = requests.get("https://chat.openai.com/")
            if response.status_code == 200:
                print("Request successful")
        except Exception as e:
            print(f"Error occurred: {e}")


@app.route('/stats')
def get_container_usage():
    try:
        # Memory usage
        memory_usage = psutil.virtual_memory().used / (1024 * 1024)  # in MB
        total_memory = psutil.virtual_memory().total / (1024 * 1024)  # in MB
        # CPU usage
        cpu_percent_usage = psutil.cpu_percent()

        # Network usage
        network_stats = psutil.net_io_counters()

        # Construct and return the dictionary
        container_usage = {
            'memory_usage_mb': {
                "Total_allocated": memory_usage,
                "Current_usage": total_memory
                },
            'cpu_percent_usage': cpu_percent_usage,
            'network_usage': {
                'bytes_sent': network_stats.bytes_sent,
                'bytes_recv': network_stats.bytes_recv,
                'packets_sent': network_stats.packets_sent,
                'packets_recv': network_stats.packets_recv
            }
        }
        return container_usage
    except Exception as e:
        print(f"Error occurred: {e}")


@app.route('/')
def hello_world():
    # res = requests.get(COUNTER_SERVICE_URL + '/get_and_increment_counter')
    duration_seconds = int(request.args.get('duration_seconds'))
    memory = request.args.get('memory_load')
    load_type = request.args.get('type_type')
    if load_type == 'cpu':
        cpu_thread = threading.Thread(target=cpu_load, args=(duration_seconds,))
        cpu_thread.start()
    elif load_type == 'memory':
        memory_thread = threading.Thread(target=memory_load, args=(memory, duration_seconds))
        memory_thread.start()
    else:
        network_thread = threading.Thread(target=network_load, args=(duration_seconds,))
        network_thread.start()
    return str(IPAddr)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
