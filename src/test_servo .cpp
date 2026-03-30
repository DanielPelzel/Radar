// #include <arduino.h>
// #include <servo.h>
//
// Servo testServo;
//
// const int servoPin = 9;
//
// void setup() {
//     testServo.attach(servoPin);
//     Serial.begin(9600);
//     Serial.println("Sende u für +10 us, send d für -10ms");
// }
//
// int currentMicros = 1500;
//
// void loop() {
//
//     if (Serial.available() > 0) {
//         char c = Serial.read();
//         if (c == 'u') {
//             testServo.writeMicroseconds(currentMicros);
//             currentMicros += 10;
//         } else if (c == 'd') {
//             testServo.writeMicroseconds(currentMicros);
//             currentMicros -= 10;
//         }
//         Serial.print("Aktueller puls: ");
//         Serial.println(currentMicros);
//
//     }
//
//
//
// }
