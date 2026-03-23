import RPi.GPIO as GPIO
import time

SW = 24  # [1] 스위치 핀
CDS = 17  # [2] 조도 센서 핀
LED = 18  # [3] LED 핀
SPKR = 25  # [4] 부저(스피커) 핀

notes = [
    391,
    391,
    440,
    440,
    391,
    391,
    330,
    330,
    391,
    391,
    330,
    330,
    294,
    294,
    294,
    0,
    391,
    391,
    440,
    440,
    391,
    391,
    330,
    330,
    391,
    330,
    294,
    330,
    262,
    262,
    262,
    0,
]

NOTE_DURATION = 0.28

# 전역 상태 변수
music_enabled = True  # 버튼으로 음악 허용/금지 토글
note_index = 0

# 조건 1    : SW 입력  => 음악 재생여부 제어
# 조건 2    : 조도센서 => 밝음 -> LED on/off 반복 / 음악 stop
# 조건 2'   : 조도세서 => 어둠 -> 부저로 음악 재생


# code 86 line -> GPIO.add_event_detect(SW, GPIO.FALLING, callback=key_handler, bouncetime=300)
# 조건 1 code 작성
def key_handler(channel):
    global music_enabled

    music_enabled = not music_enabled

    if music_enabled:
        print("음악 재생 허용")
    else:
        print("음악 재생 중지")


# 조건 2 code 작성
def buzz(freq, duration):
    """한 음을 재생.
    밝아지거나 music_enabled가 False가 되면 즉시 중단."""
    global music_enabled

    if freq == 0:
        end_time = time.time() + duration
        while time.time() < end_time:
            # 음악 멈춤 조건 -> 밝음 or sw enable
            if GPIO.input(CDS) == GPIO.HIGH or not music_enabled:
                return False
            time.sleep(0.01)
        return True

    period = 1.0 / freq
    half_period = period / 2
    cycles = int(duration / period)

    for _ in range(cycles):
        # 음악 멈춤 조건 -> 밝음 or sw enable
        if GPIO.input(CDS) == GPIO.HIGH or not music_enabled:
            GPIO.output(SPKR, GPIO.LOW)
            return False

        GPIO.output(SPKR, GPIO.HIGH)  # 소리 on
        time.sleep(half_period)
        GPIO.output(SPKR, GPIO.LOW)  # 소리 off
        time.sleep(half_period)

    return True


def cds_music_control():
    global note_index

    GPIO.setmode(GPIO.BCM)

    # 핀 모드 설정
    GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # pull up_down -> SW -> input
    GPIO.setup(CDS, GPIO.IN)  # CDS -> In
    GPIO.setup(LED, GPIO.OUT)  # LED -> out
    GPIO.setup(SPKR, GPIO.OUT)  # SPK -> out

    GPIO.output(LED, GPIO.LOW)  # 초기상태
    GPIO.output(SPKR, GPIO.LOW)  # 초기상태

    # 버튼 인터럽트 등록
    GPIO.add_event_detect(SW, GPIO.FALLING, callback=key_handler, bouncetime=300)

    print("프로그램 시작")
    print("- 어두우면 음악 재생")
    print("- 밝으면 음악 정지")
    print("- 버튼을 누르면 음악 허용/금지 전환")
    print("- 종료하려면 Ctrl+C")

    try:
        while True:
            # CDS sensor value -> LOW
            # is_dark -> Low로 설정
            is_dark = GPIO.input(CDS) == GPIO.LOW

            # 어둡고, 음악 가능이면
            if is_dark and music_enabled:
                played = buzz(notes[note_index], NOTE_DURATION)

                if played:
                    note_index = (note_index + 1) % len(notes)
            # 아니라면
            else:
                GPIO.output(SPKR, GPIO.LOW)

            # CDS sensor value -> HIGH
            # LED On/Off 반복 -> 초기에 ON state라서
            if GPIO.input(CDS) == GPIO.HIGH:
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(LED, GPIO.LOW)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")

    finally:
        GPIO.output(SPKR, GPIO.LOW)
        GPIO.cleanup()  # RESET


if __name__ == "__main__":
    cds_music_control()
