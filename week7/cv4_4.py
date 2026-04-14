
from picamera2 import Picamera2  # Picamera2 라이브러리를 불러옴
from libcamera import Transform
import cv2  # OpenCV 라이브러리를 불러옴

picam2 = Picamera2()  # Picamera2 클래스 인스턴스

preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
picam2.configure(preview_config)
picam2.start()  # 카메라 스트리밍 시작

img_no = 0

while(True):
    # 카메라로부터 이미지를 캡처하고, 배열로 반환 (OpenCV에서 바로 사용할 수 있는 형식)
    image = picam2.capture_array()

    # 카메라 영상 상하 반전
    v_image = cv2.flip(image,0)

    # OpenCV를 사용해 이미지 표시
    cv2.imshow("CAM Preview", v_image)
    
    key = cv2.waitKey(30)&0xff
    if key == 27:  # ESC Key
        break
    elif key == 115:  # 소문자 's'
        img_no = img_no + 1
        print("test"+str(img_no)+".jpg")
        
        # Take a photo and save it as "test.jpg"
        picam2.capture_file("test"+str(img_no)+".jpg")  
        
cv2.destroyAllWindows()
