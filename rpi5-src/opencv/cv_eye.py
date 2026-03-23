import numpy as np
from picamera2 import Picamera2  # Picamera2 라이브러리를 불러옴
from libcamera import Transform
import cv2  # OpenCV 라이브러리를 불러옴

face_cascade = cv2.CascadeClassifier  \
 ("/home/pi/examples/cv4/haarcascade_frontalface_default.xml")
eye_cascade =  \
 cv2.CascadeClassifier("/home/pi/examples/cv4/haarcascade_eye.xml")


picam2 = Picamera2()  # Picamera2 클래스 인스턴스
preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
picam2.configure(preview_config)
picam2.start()  # 카메라 스트리밍 시작


while(True):
    # 카메라로부터 이미지를 캡처하고, 배열로 반환 (OpenCV에서 바로 사용할 수 있는 형식)
    image = picam2.capture_array()
    
    # 카메라 영상 상하 반전
    v_image = cv2.flip(image,0)
   
    gray = cv2.cvtColor(v_image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)  # ①
    print("Number of faces detected: " + str(len(faces)))

    for (x, y, w, h) in faces:   # ②
        v_image = cv2.rectangle(v_image, (x, y), (x + w, y + h), (255, 0, 0), 1) # ③
        roi_gray = gray[y:y + h, x:x + w] # ④
        roi_color = v_image[y:y + h, x:x + w] # ⑤
        eyes = eye_cascade.detectMultiScale(roi_gray) # ⑥
        for (ex, ey, ew, eh) in eyes:  # ⑦
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1) # ⑧
            
    # OpenCV를 사용해 이미지 표시
    cv2.imshow("Eye detect", v_image)
    
    key = cv2.waitKey(30)&0xff
    if key == 27:  # ESC Key
        break
        
cv2.destroyAllWindows()


