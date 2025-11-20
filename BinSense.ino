#include <Servo.h>

// ======= Pin Definitions =======
#define IR_PIN 5
#define PROXIMITY_PIN 6
#define RAIN_DIGITAL 3
#define BUZZER_PIN 13
#define SERVO2_PIN 10   // Servo for rain

// ======= Config =======
bool INVERT_IR = true;

// ======= Globals =======
Servo myServo2;  // Servo ONLY for rain flap

int irValue = 0;
int proximityValue = 0;
int rainDigitalValue = 0;

bool systemEnabled = false;   // IR will enable this
bool rainAllowed = false;     // Rain/metal sensors active only when systemEnabled is TRUE

void setup() {
  Serial.begin(9600);

  pinMode(IR_PIN, INPUT);
  pinMode(PROXIMITY_PIN, INPUT);
  pinMode(RAIN_DIGITAL, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  myServo2.attach(SERVO2_PIN);
  myServo2.write(0);

  Serial.println("✅ System started...");
  delay(500);
}

void loop() {

  // ===== READ SENSORS =====
  irValue = digitalRead(IR_PIN);
  proximityValue = digitalRead(PROXIMITY_PIN);
  rainDigitalValue = digitalRead(RAIN_DIGITAL);

  if (INVERT_IR) {
    irValue = !irValue;
  }

  // ===== IR ENABLES SYSTEM ONLY =====
  if (irValue == HIGH) {
    systemEnabled = true;
    rainAllowed = true;
    Serial.println("🔓 IR detected → System ENABLED");
  }

  // ===== SYSTEM REMAINS OFF UNTIL IR ENABLES =====
  if (!systemEnabled) {
    Serial.println("⛔ System OFF — waiting for IR signal...");
    delay(300);
    return;
  }

  // ===== DEBUG PRINT =====
  Serial.println("--------------------------------------------");
  Serial.print("IR = "); Serial.print(irValue);
  Serial.print(" | Proximity = "); Serial.print(proximityValue);
  Serial.print(" | Rain = "); Serial.print(rainDigitalValue);
  Serial.print(" | RainAllowed = "); Serial.println(rainAllowed);

  // ===== RAIN or METAL SENSOR OPENS FLAP =====
  if (rainAllowed && (rainDigitalValue == LOW || proximityValue == HIGH)) {

    Serial.println("☔ Rain/Metal detected → Opening Flap (Servo2)");

    myServo2.write(90);
    tone(BUZZER_PIN, 1000, 300);

    delay(5000);

    myServo2.write(0);
    Serial.println("☔ Flap closed");

    rainAllowed = false;   // Disable until IR resets
    Serial.println("🚫 Rain/Metal sensors DISABLED until IR triggers again");
  }

  delay(200);
}
