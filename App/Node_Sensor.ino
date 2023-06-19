#include <WiFi.h>
#include <time.h>
#include <WiFiClient.h>
#include <WiFiServer.h>
#include <DHT.h>

#define DHTPIN 2    
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "DUC MANH";           
const char* password = "0987654321";   

const char* host = "192.168.1.123";   
const int port = 8888;    

WiFiClient client;

float humidityAverage = 0;
float temperatureAverage = 0;

unsigned long previousMillis = 0; 
const unsigned long interval = 360000;

void setup() {
  Serial.begin(115200);

  Serial.println(F("DHT11 test!"));

  dht.begin();

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
  
  if (!client.connect(host, port)) {
    Serial.println("Connection failed");
    return;
  }
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
  
    int count = 0;
    float humidity = 0;
    float temperature = 0;
    
    while(count < 10) {
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      
      if (!isnan(h) || !isnan(t)) {
        humidity += h;
        temperature += t;
        count++;
      }
  
      delay(500);
    }
  
    if (count == 0) { 
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
  
    humidityAverage = humidity / count;
    temperatureAverage = temperature / count;
  
    Serial.print(F("Temperature: "));
    Serial.print(temperatureAverage);
    Serial.print(F("°C "));
    Serial.print(F("Humidity: "));
    Serial.print(humidityAverage);
    Serial.println(F("%"));
  
    if (client.connected()) {
      String data = String(temperatureAverage) + "|" + String(humidityAverage);
      client.println(data);
  
      if (client.available()) {
        String response = client.readStringUntil('\n');
        Serial.println(response);
      }
    } 
    else {
      Serial.println("Lost connection, reconnecting...");

      while (!client.connected()) {
        if (!client.connect(host, port)) {
          Serial.println("Reconnection failed");
          delay(1000);
        }
      }
    }
  }
}
