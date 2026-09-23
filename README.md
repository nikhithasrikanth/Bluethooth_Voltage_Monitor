Bluetooth_Voltage_Monitor

This project is a Bluetooth-based voltage monitoring system developed using an Arduino UNO, HC-05 Bluetooth module, and a Python-based PC GUI. The system uses a 12 V DC supply to power the prototype, while the Arduino UNO uses its A0 analog input to measure the voltage signal, process it using its ADC, and wirelessly transmit the measured voltage to a computer.

During testing, the 12 V DC supply was connected to a buck converter, which was adjusted to provide a suitable test voltage. A 2 kΩ/1 kΩ resistor divider was then used to safely scale the test voltage before applying it to the Arduino A0 input. The measured voltage was transmitted through the HC-05 Bluetooth module using serial communication.

A Python GUI was developed using Tkinter and Matplotlib to receive and display the voltage in real time. The GUI also includes a programmable voltage/current span, calculates the corresponding current, and displays live voltage and current graphs. A clear graph function is also provided for monitoring new readings.
