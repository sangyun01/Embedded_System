import RPi.GPIO as GPIO
import time
import sys

def led_pwm_control(gpio_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pin, GPIO.OUT)

    pwm = GPIO.PWM(gpio_pin, 1000)  # 1kHz 주파수
    pwm.start(0)  # duty cycle 0%로 시작

    try:
        for i in range(10000):
            duty = i % 256  # 0~255 사이 반복
            pwm.ChangeDutyCycle(duty * 100 / 255)  # 0~100%로 변환
            time.sleep(0.005)
    finally:
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} GPIO_NO")
        sys.exit(1)

    try:
        gpio = int(sys.argv[1])
    except ValueError:
        print("GPIO 번호는 정수여야 합니다.")
        sys.exit(1)

    led_pwm_control(gpio)
