import picamera, time

Camera = picamera.PiCamera()              # 카메라 객체 생성
Camera.resolution = (1920, 1080)          # 해상도 설정
Camera.rotation = 180                     # 영상 회전
Camera.hflip = True                       # 수평 플립

Camera.start_preview()                    # 프리뷰 시작
print('Camera Start')

try:
    while True:
        input()                           # 사용자 입력 대기 (엔터키)
        str = time.ctime() + '.jpg'       # 시간 정보를 문자열로 변환
        Camera.capture(str)               # 카메라 영상 캡처
        print(str + ' file created')

except KeyboardInterrupt:                 # Ctrl+C를 누를 경우
    print('Camera Stop')
    Camera.stop_preview()                  # 카메라 프리뷰 중지
