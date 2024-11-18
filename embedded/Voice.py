from ultralytics import YOLO
import cv2
import json
def speech(text):
    import pyttsx3

    engine = pyttsx3.init()

    # Chọn giọng nói
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()

if __name__ =='__main__':

    model_1 = YOLO('best_btx.pt')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        r = model_1.predict(source=frame, conf=0.6)
        a_frame = r[0].plot()
        json_str = r[0].tojson()
        json_list = json.loads(json_str)
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow('AI-BTX',a_frame)
        if len(json_list) >= 1:
            text = 'Hello BTX Students'
            speech(text)
        else:
            text = "No btx"
            speech(text)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()