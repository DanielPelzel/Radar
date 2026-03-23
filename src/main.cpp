//
// Created by Daniel Pelzel on 23.03.26.
//
#include <Arduino.h>


//Variablen definieren
float seconds;
float distance_m;
float distance_cm;

int trig = 8;
int echo = 7;


void setup() {
    pinMode(trig, OUTPUT);
    pinMode(echo, INPUT);
    Serial.begin(9600);
}

void loop() {

    // Sicherstellen, dass der Pin vorher LOW ist
    digitalWrite(trig, LOW);
    delayMicroseconds(2);

    //Sending Input signal (10 microseconds)

    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);

    //ultrasonic wave time

    seconds = pulseIn(echo, HIGH) * 1e-6;


    //time to distance calc.

    distance_m = (seconds * 340.0 /2.0);
    distance_cm = distance_m * 100;
    Serial.println(distance_cm);



}