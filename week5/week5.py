import RPi.GPIO as GPIO
import time

# HC_SR04
TRIG = 23  # [1]
ECHO = 24  # [2]

# LED -> Setting the LED Pin
led_R = 17  # [3]
led_Y = 27  # [4]

# Servo
SERVO_PIN = 18  # [5]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# HC_SR04
# Trig -> 신호 발생 -> output
GPIO.setup(TRIG, GPIO.OUT)  # [6]
# Echo -> 발생한 신호를 다시 받음 -> input
GPIO.setup(ECHO, GPIO.IN)  # [7]

# LED -> output
GPIO.setup(led_R, GPIO.OUT)  # [8]
GPIO.setup(led_Y, GPIO.OUT)  # [9]

# servo -> motor -> output
GPIO.setup(SERVO_PIN, GPIO.OUT)  # [10]
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

print("Ultrasonic Sensor Ready")

GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

try:
    while True:
        # 초음파 트리거
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            start = time.time()

        while GPIO.input(ECHO) == 1:
            stop = time.time()

        check_time = stop - start
        distance = check_time * 34300 / 2

        print("Distance : %.1f cm" % distance)

        # LED with distance
        if distance < 20:  # [11]
            # LED RED on
            GPIO.output(led_Y, GPIO.LOW)  # Y -> off
            GPIO.output(led_R, GPIO.HIGH)  # R -> on
        else:
            GPIO.output(led_Y, GPIO.HIGH)  # Y -> on
            GPIO.output(led_R, GPIO.LOW)  # R -> off

        if distance < 20:  # [16]
            servo.ChangeDutyCycle(2.5)  # [17] # degree 0
            print("Servo : 0")
        elif 20 <= distance < 40:  # [18]
            servo.ChangeDutyCycle(7.5)  # [19] # degree 90
            print("Servo : 90")
        else:
            servo.ChangeDutyCycle(12.5)  # [20] # degree 180
            print("Servo : 180")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped by User")
    servo.stop()
    GPIO.cleanup()  # [21]
