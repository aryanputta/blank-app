/*
  Arduino capture sketch for hardware noise sampling.
  Streams analog channels for fusion with simulated telemetry.
*/

const int SENSOR_PINS[] = {A0, A1, A2, A3};
const int NUM_SENSORS = 4;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  Serial.println("timestamp_ms,ch0,ch1,ch2,ch3");
}

void loop() {
  unsigned long ts = millis();
  Serial.print(ts);
  for (int i = 0; i < NUM_SENSORS; i++) {
    int value = analogRead(SENSOR_PINS[i]);
    Serial.print(",");
    Serial.print(value);
  }
  Serial.println();
  delay(20);
}
