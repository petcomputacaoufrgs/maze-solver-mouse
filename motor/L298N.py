import RPi.GPIO as GPIO
from time import sleep

# pinos:
ENA = 18    # enable do motor A (PWM)
IN1 = 23    # os INs determinam a direção
IN2 = 24

ENB = 13
IN3 = 27
IN4 = 22

PWM_FREQ = 1000     # Hz

def setup():
    GPIO.setmode(GPIO.BCM)  #modo de pinagem
    GPIO.setwarnings(False)  #desativa warnings no terminal

    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT) # seta esses pinos como saída
    GPIO.setup([ENA, ENB], GPIO.OUT)

    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW) # inicializa 0

    pwm_a = GPIO.PWM(ENA, PWM_FREQ)     # gera objetos pwm para controlar os motores
    pwm_b = GPIO.PWM(ENB, PWM_FREQ)

    pwm_a.start(0)
    pwm_b.start(0)

    return pwm_a, pwm_b

def motor_a_forward(speed, pwm_a):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)

def motor_a_backward(speed, pwm_a):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)

def motor_a_stop(pwm_a, brake=False):
    pwm_a.ChangeDutyCycle(0)
    if brake:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.HIGH)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)

def motor_b_forward(speed, pwm_b):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_b.ChangeDutyCycle(speed)

def motor_b_backward(speed, pwm_b):
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_b.ChangeDutyCycle(speed)

def motor_b_stop(pwm_b, brake=False):
    pwm_b.ChangeDutyCycle(0)
    if brake:
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.HIGH)
    else:
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)

def all_stop(pwm_a, pwm_b, brake=False):
    motor_a_stop(pwm_a, brake=brake)
    motor_b_stop(pwm_b, brake=brake)

def cleanup(pwm_a, pwm_b):
    all_stop(pwm_a, pwm_b)
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()


pwm_a, pwm_b = setup()

try:
    print("F: forward | B: backwards | L: left | R: right | S: break | Q: quit")
    while(True):
        x = input().strip().lower()

        if x=='f':
            #forward
            print("Forward")
            motor_a_forward(60, pwm_a)
            motor_b_forward(60, pwm_b)

        elif x == 'b':
            #backward
            print("Backward")
            motor_a_backward(60, pwm_a)
            motor_b_backward(60, pwm_b)


        elif x == 'l':
            #esquerda
            print("Turn left")
            motor_a_backward(50, pwm_a)
            motor_b_forward(50, pwm_b)
        
        elif x == 'r':
            #direita
            print("Turn right")
            motor_a_forward(50, pwm_a)
            motor_b_backward(50, pwm_b)

        elif x == 's':
            #stop
            print("Break")
            all_stop(pwm_a, pwm_b, brake=True)
        
        elif x == 'q':
            #quit
            print("Quit")
            break

finally:
    cleanup(pwm_a, pwm_b)
