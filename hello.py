from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(0)
model = YOLO('best_btx.pt')
while True:
    ret, frame = cap.read()
    model.predict(source=frame,show=True)

cap.release()
cv2.destroyAllWindows()
