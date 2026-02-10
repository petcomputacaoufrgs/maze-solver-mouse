import RPi.GPIO as GPIO
from time import sleep

# pinos do motor A e do motor B, os pinos X1 são o do PWM, os X2 definem direção

A1 = 18
A2 = 23

B1 = 13
B2 = 24

PWM_FREQ = 1000  # Hz

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup([A1, A2, B1, B2], GPIO.OUT)
    GPIO.output([A1, A2, B1, B2], GPIO.LOW)

    pwm_a = GPIO.PWM(A1, PWM_FREQ)
    pwm_b = GPIO.PWM(B1, PWM_FREQ)

    pwm_a.start(0)
    pwm_b.start(0)

    return pwm_a, pwm_b

def motor_a_forward(speed, pwm_a):
    GPIO.output(A2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)

def motor_a_backward(speed, pwm_a):
    GPIO.output(A2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)

def motor_a_stop(pwm_a):
    # coast, solto
    pwm_a.ChangeDutyCycle(0)
    GPIO.output(A2, GPIO.LOW)

def motor_b_forward(speed, pwm_b):
    GPIO.output(B2, GPIO.LOW)
    pwm_b.ChangeDutyCycle(speed)

def motor_b_backward(speed, pwm_b):
    GPIO.output(B2, GPIO.HIGH)
    pwm_b.ChangeDutyCycle(speed)

def motor_b_stop(pwm_b):
    pwm_b.ChangeDutyCycle(0)
    GPIO.output(B2, GPIO.LOW)

def all_stop(pwm_a, pwm_b):
    motor_a_stop(pwm_a)
    motor_b_stop(pwm_b)

def cleanup(pwm_a, pwm_b):
    all_stop(pwm_a, pwm_b)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()

#  main
pwm_a, pwm_b = setup()

try:
    print("F: forward | B: backwards | L: left | R: right | C: coast stop | Q: quit")
    while True:
        x = input().strip().lower()

        if x == 'f':
            print("Forward")
            motor_a_forward(60, pwm_a)
            motor_b_forward(60, pwm_b)

        elif x == 'b':
            print("Backward")
            motor_a_backward(60, pwm_a)
            motor_b_backward(60, pwm_b)

        elif x == 'l':
            print("Turn left")
            motor_a_backward(50, pwm_a)
            motor_b_forward(50, pwm_b)

        elif x == 'r':
            print("Turn right")
            motor_a_forward(50, pwm_a)
            motor_b_backward(50, pwm_b)

        elif x == 'c':
            print("Coast stop")
            all_stop(pwm_a, pwm_b)

        elif x == 'q':
            print("Quit")
            break

finally:
    cleanup(pwm_a, pwm_b)
