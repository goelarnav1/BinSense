int irSensor = 2;
int rainSensor = 3;
int buzzer = 8;

void setup() {
  Serial.begin(9600);
  pinMode(irSensor, INPUT);
  pinMode(rainSensor, INPUT);
  pinMode(buzzer, OUTPUT);
  Serial.println("IR & Rain Sensor Data Started");
}

void loop() {
  int irValue = digitalRead(irSensor);
  int rainValue = digitalRead(rainSensor);

  // Fix inversion for both:
  // IR: 1 = Object Detected, 0 = No Object
  // Rain: 1 = Rain Detected, 0 = No Rain
  irValue = (irValue == 0) ? 1 : 0;
  rainValue = (rainValue == 0) ? 0 : 1;

  // Buzzer ON if either detects something
  if (irValue == 1 || rainValue == 1) {
    digitalWrite(buzzer, HIGH);
  } else {
    digitalWrite(buzzer, LOW);
  }

  Serial.print("IR:");
  Serial.print(irValue);
  Serial.print(",RAIN:");
  Serial.println(rainValue);

  delay(1000);
}
