import sys
import time
import RPi.GPIO as GPIO

STEP_PIN = 20      # S
DIR_PIN = 21       # D
EN_PIN = 16        # E

EN_ACTIVE_LOW = True      # set False if the motor doesn't respond in the test
STEPS_PER_REV = 200 * 16  # 3200: all DIP switches ON = 1/16
STEP_DELAY = 0.00005        

def enable(on):
    level = (not on) if EN_ACTIVE_LOW else on
    GPIO.output(EN_PIN, GPIO.HIGH if level else GPIO.LOW)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in (STEP_PIN, DIR_PIN, EN_PIN):
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    enable(True)

def step_n(n, forward=True):
    GPIO.output(DIR_PIN, GPIO.HIGH if forward else GPIO.LOW)
    time.sleep(0.00001)
    for _ in range(n):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY)

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    setup()
    position = 0
    try:
        sign = 1 if n > 0 else -1
        for i in range(1, abs(n) + 1):
            target = sign * round(i * 60 * STEPS_PER_REV / 360.0)
            delta = target - position
            if delta:
                step_n(abs(delta), forward=(delta > 0))
            position = target
            time.sleep(0.2)
    finally:
        enable(False)       # release the motor
        GPIO.cleanup()

if __name__ == "__main__":
    main()
