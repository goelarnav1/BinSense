// #include <Servo.h>

// // ======= Pin Definitions =======
// #define IR_PIN 5
// #define PROXIMITY_PIN 6
// #define RAIN_ANALOG A0
// #define RAIN_DIGITAL 3
// #define BUZZER_PIN 13
// #define SERVO_PIN 7
// #define SERVO2_PIN 10   // NEW SERVO (Rain only)

// // ======= Config =======
// bool INVERT_IR = true;

// // ======= Globals =======
// Servo myServo;           // Servo for object detection
// Servo myServo2;          // Servo ONLY for rain
// int irValue = 0;
// int proximityValue = 0;
// int rainAnalogValue = 0;
// int rainDigitalValue = 0;

// void setup() {
//   Serial.begin(9600);

//   pinMode(IR_PIN, INPUT);
//   pinMode(PROXIMITY_PIN, INPUT);
//   pinMode(RAIN_DIGITAL, INPUT);
//   pinMode(BUZZER_PIN, OUTPUT);

//   myServo.attach(SERVO_PIN);
//   myServo2.attach(SERVO2_PIN);

//   myServo.write(0);  
//   myServo2.write(0);

//   Serial.println("✅ System started...");
//   delay(500);
// }

// void loop() {
//   // ======= Read Sensors =======
//   irValue = digitalRead(IR_PIN);
//   proximityValue = digitalRead(PROXIMITY_PIN);
//   rainAnalogValue = analogRead(RAIN_ANALOG);
//   rainDigitalValue = digitalRead(RAIN_DIGITAL);

//   if (INVERT_IR) {
//     irValue = !irValue;
//   }

//   // ======= Debug Info =======
//   Serial.println("---------------------------------------------");
//   Serial.print("IR Sensor: ");
//   Serial.println(irValue == HIGH ? "Object Detected" : "No Object");

//   Serial.print("Proximity Sensor: ");
//   Serial.println(proximityValue == HIGH ? "Object Nearby" : "No Object");

//   Serial.print("Rain Analog Value: ");
//   Serial.println(rainAnalogValue);

//   Serial.print("Rain Digital Value: ");
//   Serial.println(rainDigitalValue == LOW ? "WET" : "DRY");

//   // ======= CONTROL LOGIC =======

//   // 1️⃣ RAIN DETECTED → Only Servo2 works with 5 sec delay
//   if (rainDigitalValue == LOW) {
//     myServo2.write(90);
//     tone(BUZZER_PIN, 1000, 400);
//     Serial.println("☔ Rain detected → Servo2 = 90°");

//     delay(5000);     // 5-second delay for servo2

//     myServo2.write(0);
//     Serial.println("↩️ Servo2 returned to 0°");
//   }

//   // 2️⃣ OBJECT DETECTED → ONLY PROXIMITY SENSOR CONTROLS SERVO1
//   if (proximityValue == HIGH) {     // ⬅️ IR removed from condition
//     myServo.write(90);
//     digitalWrite(BUZZER_PIN, HIGH);
//     Serial.println("👀 Proximity detected → Servo1 = 90°");

//     delay(5000);   // 5-second delay for servo1

//     myServo.write(0);
//     digitalWrite(BUZZER_PIN, LOW);
//     Serial.println("↩️ Servo1 returned to 0°");
//   }
//   else if (rainDigitalValue != LOW) {
//     myServo.write(0);
//     digitalWrite(BUZZER_PIN, LOW);
//   }

//   delay(600);
// }