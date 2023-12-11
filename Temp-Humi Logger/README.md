# ESP32-Humidity-Temp-Sensor
Simple esp32 Humidity and temperature that sends data to API

Certainly! To provide comprehensive documentation, I'll create sections covering the API structure, ESP32 code, and general usage instructions.

### API Documentation:

#### File Structure:
```
API/
├── static/
│   └── css/
│       └── your_css_file.css
└── templates/
    └── index.html
```

#### `index.html` (Template File):
- This file is the main HTML template for the dashboard.
- Ensure proper HTML structure, including headers, tables, and buttons.
- Use CSS for styling if needed (`your_css_file.css`).

#### CSS File:
- **File Path:** `API/static/css/your_css_file.css`
- Use this file for styling your HTML elements.
- Customize styles based on your design preferences.

#### API Endpoints:

1. **`POST /data`:**
    - **Description:** Receives sensor data from ESP32.
    - **Parameters:** Form data with sensor readings.
    - **Response:** Text confirmation or error message.

2. **`GET /dashboard`:**
    - **Description:** Displays a dashboard with sensor data.
    - **Response:** HTML page with dynamic data.

3. **`GET /export_csv`:**
    - **Description:** Exports sensor data in CSV format.
    - **Response:** CSV file download.

4. **`GET /reset_data`:**
    - **Description:** Resets all sensor data.
    - **Response:** Redirects to the dashboard.

### ESP32 Code Documentation:

#### Required Libraries:
- `WiFi.h`: For connecting to Wi-Fi.
- `DHT.h`: For interacting with DHT sensors.
- `HTTPClient.h`: For making HTTP requests.

#### Constants:
- `DHTPIN1` and `DHTPIN2`: GPIO pin numbers for DHT sensors.
- `DHTTYPE`: DHT sensor type (e.g., DHT11).
- `ssid` and `password`: Wi-Fi credentials.
- `server`: IP address of the Flask server.

#### Setup Function (`setup()`):
- Initializes serial communication.
- Connects to Wi-Fi.
- Initializes DHT sensors.

#### Loop Function (`loop()`):
- Delays for 1 minute between data transmissions.
- Reads sensor values.
- Sends data to the Flask server using HTTP POST.
- Handles success or error responses.

#### `getFormattedTimestamp` Function:
- Formats the current timestamp as `HH:MM:SS`.
- Used in constructing the data payload.

### General Usage Instructions:

1. **Flask Server:**
   - Ensure Python and Flask are installed.
   - Navigate to the `API` directory in the terminal.
   - Run `python app.py` to start the Flask server.
   - Access the dashboard at `http://192.168.43.1:5000/dashboard`.

2. **ESP32 Setup:**
   - Adjust GPIO pin numbers, Wi-Fi credentials, and server IP in the ESP32 code.
   - Upload the code to your ESP32 board using the Arduino IDE or preferred tool.

3. **Dashboard Actions:**
   - View sensor data on the dashboard.
   - Click "Export CSV" to download sensor data in CSV format.
   - Click "Reset Data" to clear all sensor data.

4. **Customization:**
   - Modify HTML, CSS, and Python code as needed.
   - Customize the structure and styling of the dashboard.
   - Adjust sensor data processing based on project requirements.

These instructions provide a high-level overview of setting up and using the system. Detailed customization and modification can be done based on specific project needs. Ensure dependencies are installed, and the ESP32 is connected to the same Wi-Fi network as the Flask server.

Feel free to adjust the documentation based on your specific project details and requirements.