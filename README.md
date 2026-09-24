# Bluetooth Voltage Monitoring System

This project is a Bluetooth-based voltage monitoring system developed using an Arduino UNO, HC-05 Bluetooth module, and a Python-based PC GUI. The system is designed to measure a 0–4 V DC analog input using the Arduino UNO A0 analog input, process the signal using its ADC, and transmit the measured voltage wirelessly to a computer.

The overall data flow is:

0–4 V Analog Input → Arduino A0 → ADC → Arduino → HC-05 → Bluetooth Wireless → PC → Python GUI

During prototype testing, a 12 V DC supply was connected to a buck converter, which was adjusted to provide a suitable test voltage. A 2 kΩ/1 kΩ resistor divider was then used to safely scale the test voltage before applying it to the Arduino A0 input.

For the intended 0–4 V input, the signal can be applied directly to A0 when the input is verified to be within the Arduino's safe analog input range.


## Voltage Measurement

The Arduino UNO uses a 10-bit ADC, providing values from 0 to 1023.

The voltage is calculated using:

Voltage = ADC Reading × 5 / 1023

During prototype testing, the resistor divider was used to scale the higher test voltage before applying it to A0.

The measured voltage was then formatted and transmitted to the HC-05.

## Serial and Bluetooth Communication

The Arduino and HC-05 communicate using serial communication through the TX and RX pins.

- Arduino pin 11 (TX) sends serial data to the HC-05 RXD.
- HC-05 TXD sends data to Arduino pin 10 (SoftwareSerial RX).
- The Arduino sends the measured voltage to the HC-05 as serial data.
- The HC-05 transmits the received data wirelessly to the PC using Bluetooth.
- The Python GUI receives the Bluetooth serial data and displays the measured voltage.

Therefore, the communication path is:

Arduino → Serial TX/RX → HC-05 → Bluetooth Wireless → PC → Python GUI

The HC-05 provides the wireless communication link for transmitting measurement data from the Arduino to the computer. During prototype development, the Arduino is also connected to the Mac via USB for power, programming and serial/debugging purposes. The measurement data displayed in the Python GUI is received through the HC-05 Bluetooth connection.

## Python GUI

A Python GUI was developed using Tkinter and Matplotlib to receive and display the voltage in real time.

The GUI provides:

- Live voltage display
- Programmable voltage/current span
- Calculated current display
- Live voltage graph
- Live current graph
- Bluetooth connection status
- Clear Graph function

The GUI calculates the corresponding current based on the programmed voltage/current span.

The current is calculated using:

Current = Voltage × (Maximum Current / Maximum Voltage)

The current displayed by the GUI is calculated from the measured voltage; it is not directly measured using a current sensor in this prototype.

## Testing

The prototype was tested by changing the physical test voltage using the buck converter.

The Arduino measured the voltage at A0, transmitted the measured value through the HC-05, and the Python GUI received and displayed the voltage and corresponding calculated current.


