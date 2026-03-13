/*
  Arduino Uno capture sketch for hybrid-noise collection.
  Sensors: DHT22 temperature, MPU-6050 vibration proxy, voltage divider, extra analog channel.
  Sampling: 10 Hz serial stream for downstream CSV logging.
*/

const int TEMP_PIN = A0;      // DHT22 analog proxy channel
const int MPU_PIN = A1;       // MPU-6050 vibration proxy channel
const int VOLTAGE_PIN = A2;   // Voltage divider input
const int AUX_PIN = A3;       // Auxiliary noise channel

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  Serial.println("timestamp_ms,ch0,ch1,ch2,ch3");
}

void loop() {
  unsigned long ts = millis();
  int dht_raw = analogRead(TEMP_PIN);
  int mpu_raw = analogRead(MPU_PIN);
  int voltage_raw = analogRead(VOLTAGE_PIN);
  int aux_raw = analogRead(AUX_PIN);

  Serial.print(ts);
  Serial.print(",");
  Serial.print(dht_raw);
  Serial.print(",");
  Serial.print(mpu_raw);
  Serial.print(",");
  Serial.print(voltage_raw);
  Serial.print(",");
  Serial.println(aux_raw);

  delay(100); // 10 Hz
}
