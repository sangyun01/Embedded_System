import RPi.GPIO as GPIO
from time import sleep

def KeyHandler(n):			# 인터럽트 서비스 함수
	print("Key is pressed [%d]" %n)

PIN = 24
GPIO.setmode(GPIO.BCM)			# 핀 번호를 BCM 모드로 설정
GPIO.setup(PIN, GPIO.IN)		# 24번 핀을 입력 모드로 설정

# 인터럽트 서비스 함수 등록
GPIO.add_event_detect(PIN, GPIO.FALLING, callback=KeyHandler)

sec = 0
try:
    while True:				# 1초에 한 번씩 문자열 출력
        print("sec : %d" %sec)
        sec = sec + 1
        sleep(1)

except KeyboardInterrupt:		# Ctrl+C 누르면 GPIO 초기화 및 프로그램 종료
    print("\n프로그램을 종료합니다.")
    GPIO.cleanup()
