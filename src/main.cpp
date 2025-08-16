#include "photodiode.h"
#include "emitter.h"
#include "mpu6050.h"
#include "bluetooth.h"

Photodiode photodiode(2);    // GPIO2 for ADC
Emitter irLED(3);            // GPIO3 for PWM
BluetoothManager bt;
MPU6050 mpu;

void setup() {
  Serial.begin(115200);

  irLED.begin();
  irLED.setDutyPercent(50);
  photodiode.begin();

  mpu.begin(6, 7); // SDA = GPIO6, SCL = GPIO7

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
  }

  bt.begin("AntiSleepGlasses");
  Serial.println("Bluetooth Started. Waiting for connections...");

  // ✅ Print CSV header for logging
  Serial.println("timestamp,raw_voltage,ax,ay,az");
}

void loop() {
  int raw = photodiode.readRaw();
  float voltage = photodiode.readVoltage();
  int16_t ax, ay, az;

  if (mpu.testConnection()) {   // ✅ Only stream if MPU is online
    mpu.getAcceleration(&ax, &ay, &az);

    // ✅ Skip null data (all zeros usually means bad read)
    if (!(ax == 0 && ay == 0 && az == 0)) {
      unsigned long ts = millis();

      // --- Normal debug prints ---
      Serial.printf("Raw: %d\tVoltage: %.2f V\n", raw, voltage);
      Serial.printf("AX:%d,AY:%d,AZ:%d\n", ax, ay, az);

      // --- CSV formatted line ---
      Serial.print(ts); Serial.print(",");
      Serial.print(voltage, 2); Serial.print(",");
      Serial.print(ax); Serial.print(",");
      Serial.print(ay); Serial.print(",");
      Serial.println(az); // newline ends the CSV row

      // --- Send same data over Bluetooth ---
      String sensorData = "Raw:" + String(raw) + 
                          "\tVoltage:" + String(voltage) + "V\t" +
                          "AX:" + String(ax) + ",AY:" + String(ay) + ",AZ:" + String(az);
      bt.send(sensorData);
    }
  } else {
    Serial.println("MPU offline, pausing data stream...");
    delay(1000); // wait before retrying
  }

  // --- Bluetooth receive handler ---
  if (bt.available()) {
    String received = bt.receive();
    Serial.print("Received via BT: ");
    Serial.println(received);
  }

  delay(200); // sampling rate
}
