import RPi.GPIO as GPIO
import time

# 핀 정의 (BCM 번호 기준)
SW = 24    # 스위치 (GPIO24) - 실제 코드에서는 사용되지 않음
CDS = 17   # 조도 센서 (GPIO17)
LED = 18   # LED (GPIO18)

def cds_control():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW, GPIO.IN)       # 스위치 (사용되지 않지만 포함)
    GPIO.setup(CDS, GPIO.IN)      # 조도 센서
    GPIO.setup(LED, GPIO.OUT)     # LED 출력

    print("조도 센서 상태를 감지합니다. 종료하려면 Ctrl+C")

    try:
        while True:
            if GPIO.input(CDS) == GPIO.HIGH:  # 빛이 감지됨
                GPIO.output(LED, GPIO.HIGH)   # LED ON
                time.sleep(1)
                GPIO.output(LED, GPIO.LOW)    # LED OFF
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    cds_control()
