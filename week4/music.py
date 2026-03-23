import RPi.GPIO as GPIO
import time

SPKR = 25  # GPIO25 (wiringPi 기준 6번 핀)

# 학교 종이 땡땡땡 음계 (Hz 기준, 일부는 부동소수점이므로 round 처리)
notes = [
    391, 391, 440, 440, 391, 391, 330, 330,
    391, 391, 330, 330, 294, 294, 294, 0,
    391, 391, 440, 440, 391, 391, 330, 330,
    391, 330, 294, 330, 262, 262, 262, 0
]

def buzz(frequency, duration):
    """지정된 주파수로 버저를 울림"""
    if frequency == 0:
        time.sleep(duration)
        return

    period = 1.0 / frequency
    half_period = period / 2
    cycles = int(duration / period)

    for _ in range(cycles):
        GPIO.output(SPKR, GPIO.HIGH)
        time.sleep(half_period)
        GPIO.output(SPKR, GPIO.LOW)
        time.sleep(half_period)

def play_music():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPKR, GPIO.OUT)

    try:
        for freq in notes:
            buzz(freq, 0.28)  # 각 음을 280ms 동안 연주
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    play_music()
