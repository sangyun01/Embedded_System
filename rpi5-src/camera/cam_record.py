import picamera, time

Camera = picamera.PiCamera()              # pi 카메라 객체 생성
Camera.framerate = 30                     # 프레임 속도 설정
Camera.resolution = (1920, 1080)          # 해상도 설정
Camera.rotation = 180                     # 영상 회전
Camera.hflip = True                       # 수평 플립

# 카메라 영상을 h264 코덱으로 압축하여 파일로 저장
Camera.start_recording('/home/pi/camera/rec.h264', format='h264')
print('Camera Recording Start')

try:
    while True:
        print('frame number : %d' % Camera.frame.index)
        time.sleep(1)

except KeyboardInterrupt:   # Ctrl+C 키를 눌러 녹화 중지
    print('Camera Recording Stop')
    Camera.stop_recording()
