/**
 *@file RadarScanner
 *@author Daniel Pelzel
 *@brief measure Distance with HC-SR04 and Servo SG90 control
 */


#include <Arduino.h>
#include <Servo.h>

Servo servo;

const uint8_t trig = 8; ///< Trigger pin for ultrasonic sensor (output)
const uint8_t echo = 7; ///< echo pin for ultrasonic sensor (input)
const uint8_t servo_pin = 9; ///< PWN-Signal for SG90 Servo


/**
 * Measures the distance to an object using an ultrasonic sensor.
 *
 * This function sends a trigger pulse through the trig pin of the ultrasonic sensor,
 * receives the echo signal through the echo pin, and calculates the distance based on
 * the time it takes for the signal to return. The calculation assumes that sound travels
 * at a speed of 340 m/s in air.
 *
 * @return The measured distance in centimeters.
 */
float measure_distance() {

    // Sicherstellen, dass der Pin vorher LOW ist
    digitalWrite(trig, LOW);
    delayMicroseconds(2);

    //Sending Input signal (10 microseconds)
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);

    //ultrasonic wave time
    float seconds = pulseIn(echo, HIGH) * 1e-6;

    //time to distance calc.
    float distance_m = (seconds * 340.0 /2.0);
    float distance_cm = distance_m * 100;

    return distance_cm;
}

/**
 * @brief sends important data to SerialMonitor
 * @param angle
 * @param distance
 */
void sendData(int angle, float distance) {
    Serial.print(angle);
    Serial.print(", ");
    Serial.println(distance);
}

/**
 * @brief moves the servo to a defined angle
 * @param angle
 */
void turn(int angle) {



    servo.write(angle);

}



void setup() {
    pinMode(trig, OUTPUT);
    pinMode(echo, INPUT);
    pinMode(servo_pin, OUTPUT);
    servo.attach(9, 544, 2831);
    
    Serial.begin(9600);



}

void loop() {

    for (int angle = 10; angle < 145; angle++){
        turn(angle);

        delay(30);
        float distance = measure_distance();
        sendData(angle, distance);
    }

    for (int angle = 145; angle > 10; angle--){
        turn(angle);

        delay(30);
        float distance = measure_distance();
        sendData(angle, distance);
    }

}



