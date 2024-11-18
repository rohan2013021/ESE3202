from machine import Pin, time_pulse_us
import time

# Define pins for the HC-SR04 sensor
TRIG_PIN = 2
ECHO_PIN = 4

# RGB LED Pins
RED_PIN = 25
GREEN_PIN = 26
BLUE_PIN = 27

# Threshold for water level in cm
WATER_LEVEL_THRESHOLD = 50
MAXIMUM_WATER_LEVEL = 200

# Setup HC-SR04
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# Setup RGB LED
red = Pin(RED_PIN, Pin.OUT)
green = Pin(GREEN_PIN, Pin.OUT)
blue = Pin(BLUE_PIN, Pin.OUT)


# Function to measure distance
def measure_distance():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    duration = time_pulse_us(echo, 1, 30000)  # Timeout after 30ms if no response
    if duration == -1:
        return None  # Indicates timeout

    distance_cm = (duration / 2) / 29.1
    return distance_cm


# Function to set RGB LED color
def set_rgb(red_state, green_state, blue_state):
    red.value(red_state)
    green.value(green_state)
    blue.value(blue_state)


# Main control loop
prev_distance = None
motor_on = False
set_rgb(0, 1, 1)

while True:
    distance = measure_distance()

    if distance is not None:
        if motor_on:
            if distance > MAXIMUM_WATER_LEVEL:
                motor_on = False
                set_rgb(0, 1, 1)  # Red: Motor off
            elif distance < prev_distance:
                motor_on = False
                set_rgb(
                    1, 1, 0
                )  # Blue: Motor off, water level is not increaseing, requires priming.
        elif distance < WATER_LEVEL_THRESHOLD:
            motor_on = True
            set_rgb(1, 0, 1)  # Green: Motor on, filling

        prev_distance = distance
    else:
        print("Error: Could not measure distance")

    time.sleep(1)  # Wait 1 second before next measurement

# print("Hello!")

# Features to add:
