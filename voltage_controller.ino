// --------------------------------
// Bluetooth Voltage Monitor
// --------------------------------

// Reads the input voltage using Arduino analog pin A0 and transmits the measured voltage through the HC-05 Bluetooth module

#include <SoftwareSerial.h>

// Arduino pin 10 receives data from HC-05 TXD and Arduino pin 11 sends data to HC-05 RXD
SoftwareSerial bluetooth(10, 11);  

// Arduino UNO uses approximately 5 V as the ADC reference
const float referenceVoltage = 5.0;

// Arduino UNO has a 10-bit ADC (2^10 - 1 = 1023).
const int adcMax = 1023;

void setup() {

  // Start communication with the Arduino Serial Monitor
  Serial.begin(9600);

  // Start communication with the HC-05 Bluetooth module
  bluetooth.begin(9600);
}

void loop() {

  // Read the analog voltage connected to A0
  int raw = analogRead(A0);

  // Convert the ADC reading into voltage
  float voltage = raw * (referenceVoltage / adcMax);

  Serial.print("A0 = ");
  Serial.print(raw);

  Serial.print("   Voltage = ");
  Serial.print(voltage, 2);

  Serial.println(" V");

  // Send Voltage Through HC-05 
  bluetooth.print("Voltage = ");
  bluetooth.print(voltage, 2);
  bluetooth.println(" V");

  // Wait for 1 second before taking the next reading
  delay(1000);
}
