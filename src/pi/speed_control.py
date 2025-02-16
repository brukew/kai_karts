import RPi.GPIO as GPIO

# Define your GPIO pin numbers (adjust to your wiring)
SLOW_PIN = 17
HALT_PIN = 27
STOP_PIN = 4

# Setup GPIO - Initialized at full speed
GPIO.setmode(GPIO.BCM)
GPIO.setup(SLOW_PIN, GPIO.OUT)
GPIO.setup(HALT_PIN, GPIO.OUT)
GPIO.output(SLOW_PIN, GPIO.LOW)
GPIO.output(HALT_PIN, GPIO.LOW)
GPIO.output(STOP_PIN, GPIO.LOW)

def full_speed():
    # Equivalent to: digitalWrite(HALT_PIN, LOW); digitalWrite(SLOW_PIN, LOW); digitalWrite(D2, LOW);
    GPIO.output(HALT_PIN, GPIO.LOW)
    GPIO.output(SLOW_PIN, GPIO.LOW)
    GPIO.output(STOP_PIN, GPIO.LOW)

def three_quarters_speed():
    # Equivalent to: digitalWrite(HALT_PIN, LOW); digitalWrite(SLOW_PIN, HIGH); digitalWrite(D2, LOW);
    GPIO.output(HALT_PIN, GPIO.LOW)
    GPIO.output(SLOW_PIN, GPIO.HIGH)
    GPIO.output(STOP_PIN, GPIO.LOW)

def half_speed():
    # Equivalent to: digitalWrite(SLOW_PIN, LOW); digitalWrite(HALT_PIN, HIGH); digitalWrite(D2, LOW);
    GPIO.output(SLOW_PIN, GPIO.LOW)
    GPIO.output(HALT_PIN, GPIO.HIGH)
    GPIO.output(STOP_PIN, GPIO.LOW)

def no_speed():
    GPIO.output(SLOW_PIN, GPIO.HIGH)
    GPIO.output(HALT_PIN, GPIO.HIGH)
    GPIO.output(STOP_PIN, GPIO.HIGH)
