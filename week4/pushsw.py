import RPi.GPIO as GPIO
import time

SW = 24   # GPIO24 (wiringPi 기준 5번 핀)
LED = 18  # GPIO18 (wiringPi 기준 1번 핀)

def switch_control():
    GPIO.setmode(GPIO.BCM)      # BCM 번호 체계 사용
    GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 스위치 입력 (풀업)
    GPIO.setup(LED, GPIO.OUT)   # LED 출력

    print("스위치를 눌러 LED를 켜보세요. 종료하려면 Ctrl+C")

    try:
        while True:
            if GPIO.input(SW) == GPIO.LOW:  # 버튼이 눌렸을 때
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(LED, GPIO.LOW)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    switch_control()
