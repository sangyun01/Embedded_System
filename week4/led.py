import RPi.GPIO as GPIO
import time
import sys

def led_control(gpio):
    GPIO.setup(gpio, GPIO.OUT)

    for _ in range(5):
        GPIO.output(gpio, GPIO.HIGH)  # LED ON
        time.sleep(1)                 # 1초 대기
        GPIO.output(gpio, GPIO.LOW)   # LED OFF
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} GPIO_NO")
        sys.exit(1)

    try:
        gpio_no = int(sys.argv[1])
    except ValueError:
        print("GPIO 번호는 정수로 입력해야 합니다.")
        sys.exit(1)

    GPIO.setmode(GPIO.BCM)  # BCM 모드 사용
    GPIO.setwarnings(False)

    try:
        led_control(gpio_no)
    finally:
        GPIO.cleanup()
