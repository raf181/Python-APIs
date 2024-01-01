#include <WiFiManager.h> // Include the WiFiManager library
#include <DHT.h>
#include <HTTPClient.h>

#define DHTPIN1 12
#define DHTPIN2 13
#define DHTTYPE DHT11

DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

const char* server = "192.168.43.1";

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Create an instance of WiFiManager
  WiFiManager wifiManager;

  // Uncomment the line below to reset WiFi settings (useful during development)
  // wifiManager.resetSettings();

  // Connect to WiFi or start a configuration portal if not connected
  if (!wifiManager.autoConnect("AutoConnectAP")) {
    Serial.println("Failed to connect and hit timeout");
    delay(3000);
    // Reset and try again or put your code to handle the failure
    ESP.restart();
  }

  Serial.println("Connected to WiFi");

  dht1.begin();
  dht2.begin();
}

void loop() {
  delay(60000);

  float temperature1 = dht1.readTemperature();
  float humidity1 = dht1.readHumidity();
  float temperature2 = dht2.readTemperature();
  float humidity2 = dht2.readHumidity();

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
  time_t now;
  struct tm timeinfo;
  char timestamp[30];
  
  time(&now);
  localtime_r(&now, &timeinfo);
  strftime(timestamp, sizeof(timestamp), "%d %H:%M:%S", &timeinfo);
  
  return String(timestamp);
}