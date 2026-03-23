
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

model.train(data='G:\\products\\projects\\인공지능자동차\PI5_V\\sw\\examples\\yolo_v11\\datasets\\traffic\\data.yaml', epochs=30, patience=3, imgsz=320)

print(type(model.names), len(model.names))
print(model.names)

