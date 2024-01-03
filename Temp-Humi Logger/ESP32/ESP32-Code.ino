#include <WiFiManager.h>
#include <DHT.h>
#include <HTTPClient.h>

#define DHTPIN1 12
#define DHTPIN2 13
#define DHTTYPE DHT11

DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

const char* server = "api.raf-181.tech";
const char* apiEndpoint = "/data";
const char* username = "esp32";  // Replace with your actual username
const char* password = "sensor$295$sensor";  // Replace with your actual password

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFiManager wifiManager;
  
  if (!wifiManager.autoConnect("AutoConnectAP")) {
    Serial.println("Failed to connect and hit timeout");
    delay(3000);
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
  
  http.begin("http://" + String(server) + ":5000" + apiEndpoint);
  
  // Add basic authentication credentials to the HTTP header
  http.setAuthorization(username, password);

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
