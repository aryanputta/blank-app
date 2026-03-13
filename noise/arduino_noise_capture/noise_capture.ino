#include <Wire.h>

// DHT22 on D2 (digital), MPU-6050 over I2C, voltage divider on A0.
const int DHT_PIN = 2;
const int VOLTAGE_PIN = A0;
const int MPU_ADDR = 0x68;

float baselineTemp = 0.0;
float baselineAccel = 0.0;
float baselineVolt = 0.0;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  baselineTemp = 0.0;
  baselineAccel = 0.0;
  baselineVolt = 512.0;
}

void loop() {
  // Read MPU-6050 accelerometer X axis.
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);

  int16_t ax = Wire.read() << 8 | Wire.read();
  Wire.read(); Wire.read();
  Wire.read(); Wire.read();

  // DHT22 placeholder analog-like proxy from digital pin state for simple capture loop.
  int dhtProxy = digitalRead(DHT_PIN) * 100;
  int voltRaw = analogRead(VOLTAGE_PIN);

  float tempNoise = dhtProxy - baselineTemp;
  float accelNoise = (float)ax - baselineAccel;
  float voltNoise = (float)voltRaw - baselineVolt;

  Serial.print(millis());
  Serial.print(",");
  Serial.print(tempNoise);
  Serial.print(",");
  Serial.print(accelNoise);
  Serial.print(",");
  Serial.println(voltNoise);

  delay(100);
}
