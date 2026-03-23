import RPi.GPIO as GPIO
import time

SPKR = 12  # BCM 12번 핀

# 학교 종이 땡땡땡 음계
notes = [
    391, 391, 440, 440, 391, 391, 330, 330,
    391, 391, 330, 330, 294, 294, 294, 0,
    391, 391, 440, 440, 391, 391, 330, 330,
    391, 330, 294, 330, 262, 262, 262, 0
]

def play_music():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPKR, GPIO.OUT)

    pwm = GPIO.PWM(SPKR, 440)  # 초기 주파수는 임의값
    pwm.start(0)  # 처음에는 소리 끔

    try:
        for freq in notes:
            if freq == 0:
                pwm.ChangeDutyCycle(0)  # 쉼표
            else:
                pwm.ChangeFrequency(freq)  # 주파수 변경
                pwm.ChangeDutyCycle(50)   # 50% duty (표준)

            time.sleep(0.28)

        pwm.ChangeDutyCycle(0)

    finally:
        pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    play_music()
