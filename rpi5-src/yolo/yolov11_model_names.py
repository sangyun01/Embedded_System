
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

print(type(model.names), len(model.names))
print(model.names)
