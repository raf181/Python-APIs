#include <WiFi.h>
extern "C" {
  #include "esp_wpa2.h" // Include the header for the esp_wpa2 library
}
#include <DHT.h>
#include <HTTPClient.h>

#define DHTPIN1 12 // Replace with your ESP32 GPIO pin number
#define DHTPIN2 13 // Replace with your ESP32 GPIO pin number
#define DHTTYPE DHT11

DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

const char* ssid = "testwifi"; // Replace with your WiFi SSID
const char* username = "testuser"; // Replace with your WiFi username
const char* password = "testpassword"; // Replace with your WiFi password
const char* server = "192.168.43.1"; // Replace with your server IP address

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi
  WiFi.disconnect(true);
  WiFi.mode(WIFI_STA);

  esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)username, strlen(username));
  esp_wifi_sta_wpa2_ent_set_username((uint8_t *)username, strlen(username));
  esp_wifi_sta_wpa2_ent_set_password((uint8_t *)password, strlen(password));
  esp_wpa2_config_t config = WPA2_CONFIG_INIT_DEFAULT();
  esp_wifi_sta_wpa2_ent_enable(&config);

  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  dht1.begin();
  dht2.begin();
}

void loop() {
  delay(1000); //60000 Wait for 1 minute before sending new data

  // Reading sensor values
  float temperature1 = dht1.readTemperature();
  float humidity1 = dht1.readHumidity();
  float temperature2 = dht2.readTemperature();
  float humidity2 = dht2.readHumidity();

  // Sending data to the server
  HTTPClient http;
  http.begin("http://" + String(server) + ":5000/data");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  String postData = "timestamp=" + String(getFormattedTimestamp()) +
                    "&temperature1=" + String(temperature1) +
                    "&humidity1=" + String(humidity1) +
                    "&temperature2=" + String(temperature2) +
                    "&humidity2=" + String(humidity2);

  int httpResponseCode = http.POST(postData);
  if (httpResponseCode > 0) {
    Serial.println("Data sent successfully");
  } else {
    Serial.print("Error sending data. HTTP response code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

String getFormattedTimestamp() {
  // Get the current date and time
  time_t now;
  struct tm timeinfo;
  char timestamp[30];
  
  time(&now);
  localtime_r(&now, &timeinfo);
  strftime(timestamp, sizeof(timestamp), "%d %H:%M:%S", &timeinfo);
  
  return String(timestamp);
}
