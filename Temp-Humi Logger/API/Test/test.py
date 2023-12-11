import time
import requests
from datetime import datetime
import random

# Replace these values with your server information
server_address = "http://127.0.0.1:5000/data"

# Function to simulate sensor readings with variability
def simulate_sensor_readings():
    # Simulating DHT sensor readings with random fluctuations
    base_temperature1 = 25.0
    base_humidity1 = 50.0
    base_temperature2 = 26.0
    base_humidity2 = 55.0

    temperature1 = base_temperature1 + random.uniform(-1, 1)
    humidity1 = base_humidity1 + random.uniform(-5, 5)
    temperature2 = base_temperature2 + random.uniform(-1, 1)
    humidity2 = base_humidity2 + random.uniform(-5, 5)

    return temperature1, humidity1, temperature2, humidity2

# Function to simulate sending data to the server
def send_data_to_server():
    timestamp = datetime.now().strftime("%d %H:%M:%S")
    temperature1, humidity1, temperature2, humidity2 = simulate_sensor_readings()

    payload = {
        "timestamp": timestamp,
        "temperature1": temperature1,
        "humidity1": humidity1,
        "temperature2": temperature2,
        "humidity2": humidity2,
    }

    try:
        response = requests.post(server_address, data=payload)
        response.raise_for_status()
        print("Data sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

# Main loop to simulate continuous data sending
def main():
    while True:
        send_data_to_server()
        time.sleep(5)  # Wait for 1 minute before sending new data

if __name__ == "__main__":
    main()
