#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <ArduinoJson.h>


Adafruit_MLX90614 mlx = Adafruit_MLX90614();


float temperatureSensor = 0;
int highTemperatureSetting = 30;
int lowTemperatureSetting = 15;

int fanSpeed = 100;


void SendDataSensor();
void ReadSetting();
void ControlFanandLed();

#define in1 2
#define in2 3
#define in3 4
#define in4 5


void setup() {

  Serial.begin(9600);
  while (!Serial) continue;
  mlx.begin();  
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}
void ReadSetting()
{
  StaticJsonDocument<200> doc;

  String json = Serial.readString();

  DeserializationError error = deserializeJson(doc, json);

  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    return;
  }
  const char* sensor = doc["status"];
  int highTemp = doc["data1"];
  int lowTemp = doc["data2"];
  int speedFan = doc["data3"];
  highTemperatureSetting = highTemp;
  lowTemperatureSetting = lowTemp;
  fanSpeed = speedFan;

}
void SendDataSensor()
{
  
  StaticJsonDocument<200> doc;
  temperatureSensor = mlx.readAmbientTempC();
  doc["temperature"] = temperatureSensor;

  serializeJson(doc, Serial);
}

void ControlFanandLed()
{
 if( temperatureSensor >  highTemperatureSetting)
 {
  digitalWrite(in1, LOW);
  analogWrite(in2, 2 * fanSpeed);

  
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
 }
 if( temperatureSensor <  lowTemperatureSetting)
 {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
 }
 
}
void loop() {
  SendDataSensor();
  if(Serial.available()>0)
  {
    ReadSetting();
  }
  ControlFanandLed();
  delay(1000);
}
