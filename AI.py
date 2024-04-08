from ultralytics import YOLO
import cv2

model = YOLO('best_btx.pt')

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    results = model.predict(source=frame)
    a_frame = results[0].plot()
    
    a_frame = cv2.resize(a_frame, (640, 480))

    cv2.imshow('btx',a_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
