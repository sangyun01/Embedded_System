import cv2
import time
from ultralytics import YOLO

from picamera2 import Picamera2

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Open ONNX  model
# model = YOLO("yolo11l-seg.onnx")
model = YOLO("yolo11n_ncnn_model")

# Initialize FPS
prev_time = 0
fps = 0

while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

    # Hitung FPS
    current_time = time.time()
    elapsed_time = current_time - prev_time
    prev_time = current_time
    if elapsed_time > 0:
        fps = 1 / elapsed_time

    # Object detect
    results = model(frame)

    # Get Object frame
    annotated_frame = results[0].plot()
    
    # Print detected objects classes
    for result in results:
        for box in result.boxes:
            print(result.names[int(box.cls[0])])
            
            # cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
            #               (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
            # cv2.putText(img, f"{result.names[int(box.cls[0])]}",
            #             (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
            #             cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)     

    # Frame and FPS output
    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.2f}",
        (10, 30),  # Position (x, y)
        cv2.FONT_HERSHEY_SIMPLEX,  # Font
        1,
        (0, 255, 0),  # Warna (B, G, R)
        2,
        cv2.LINE_AA  # Line 
    )

    # Image output
    cv2.imshow("YOLO Real-time Detection", annotated_frame)

    # input 'q', exit program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
