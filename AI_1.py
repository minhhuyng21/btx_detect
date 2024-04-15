from ultralytics import YOLO
import cv2
import json
import threading 
import queue
import time
from Voice import speech 
import serial

r = False
b = False

def human_detect(frame, model):
    results = model.predict(source=frame, classes=[0])
    a_frame = results[0].plot()
    json_str = results[0].tojson()
    json_list = json.loads(json_str)
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Ready',a_frame)
    if len(json_list) >= 1:
        return True
    return False

def btx_detect(source, model):
    results = model.predict(source=source , conf=0.6)
    a_frame = results[0].plot()
    json_str = results[0].tojson()
    json_list = json.loads(json_str)
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    # cv2.imshow('Prediction', a_frame)
    # results[0].save('Prediction.jpg')
    if len(json_list) >= 1:
        return True, a_frame
    return False, a_frame

def run_thread(thread_name, arg1, arg2, wait):
    thread_run = threading.Thread(target=thread_name, args=(arg1,arg2,)) 
    thread_run.start()
    if wait:
        thread_run.join()

def predicting(source,model):
    global b, r
    print('Start detecting...')
    prediction, img =  btx_detect(source, model)
    if prediction:
        text = 'Hello BTX student'
    else:
        text = 'Not BTX student'
    cv2.imshow('Prediction', img)
    speech(text)
    time.sleep(5)
    b = False
    pass

def processing(cap, model):
    global b, r
    print('Start processing...')
    sec_count = 0
    p = False
    while sec_count < 5 and r:
        time.sleep(1)
        #TODO graphic
        sec_count += 1
        print(sec_count)
    if sec_count == 5:
        img = cap.read()
        # cv2.imshow('Image',img)
        p = True
    print('Done processing')
    if p:
        run_thread(predicting, arg1=img, arg2=model, wait=True)
    
if __name__ == '__main__':
    model_0 = YOLO('yolov8n-face.pt')
    model_1 = YOLO('best_btx.pt')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        r = human_detect(frame, model_0)
        # r = btx_detect(cap, model_1)
        print(r)
        if r and b == False:
            b = True
            run_thread(processing, arg1=cap, arg2=model_1, wait=False)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    