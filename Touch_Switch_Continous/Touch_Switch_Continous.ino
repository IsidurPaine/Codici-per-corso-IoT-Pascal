/*
  A simple code to read input from a touch sensor
  connected to pin 7 of an Arduino Uno board.
  If the sensor is touched, the built-in LED is turned on
  and a message is printed to the serial monitor.
  If the sensor is not touched, the LED is turned off
  and a different message is printed.

  Board: Arduino Uno R4 (or R3)
  Component: Touch Sensor
*/

// Define the pin used for the touch sensor
const int sensorPin = 7;
int currentState;

void setup() {
  pinMode(sensorPin, INPUT);     // Set the sensor pin as input
  pinMode(LED_BUILTIN, OUTPUT);  // Set the built-in LED pin as output
  digitalWrite(LED_BUILTIN, LOW);  // Turn off the built-in LED
  Serial.begin(9600);            // Start the serial communicatio
}

void loop() {
  currentState = digitalRead(sensorPin);
  
  if (currentState == 1) {  // If the sensor is touched
    digitalWrite(LED_BUILTIN, HIGH);  // Turn on the built-in LED
    Serial.println("1");
  }
  
  if (currentState == 0) {
    digitalWrite(LED_BUILTIN, LOW);  // Turn off the built-in LED
    Serial.println("0");
  }

  delay(100);  // Wait for a short period to avoid rapid reading of the sensor
}