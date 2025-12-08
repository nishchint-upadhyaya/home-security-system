#define BUTTON_PIN 2

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // Button on shield is active LOW
  Serial.println("TinyML Shield Button Test Started");
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("Button is PRESSED");
    delay(300);  // Simple debounce and prevents spamming Serial Monitor
  }
}