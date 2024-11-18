from ultralytics import YOLO
import cv2
import json
import threading 
import queue
import time
from embedded.Voice import speech 
import serial

ser = ''
def initialize_serial():
    port = "COM5" 
    baudrate = 115200
    stopbits = serial.STOPBITS_ONE
    bytesize = serial.EIGHTBITS
    serial_connection = serial.Serial(port, baudrate,stopbits=stopbits, bytesize=bytesize)
    return serial_connection

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

def btx_detect_rt(frame, model):
    results = model.predict(source=frame , conf=0.6)
    a_frame = results[0].plot()
    json_str = results[0].tojson()
    json_list = json.loads(json_str)
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('AI-BTX',a_frame)
    if len(json_list) >= 1:
        return True
    return False

def run_thread(thread_name, arg1, arg2, wait):
    thread_run = threading.Thread(target=thread_name, args=(arg1,arg2,)) 
    thread_run.start()
    if wait:
        thread_run.join()

def predicting(source,model):
    global b, r, ser
    print('Start detecting...')
    prediction, img =  btx_detect(source, model)
    if prediction:
        transmit_data(ser, True)
        text = 'Hello BTX student'
    else:
        transmit_data(ser, False)
        text = 'Not BTX student'
    cv2.imshow('Prediction', img)
    speech(text)
    time.sleep(5)
    b = False
    pass

def processing(cap, model):
    global b, r, ser
    print('Start processing...')
    sec_count = 0
    p = False
    while sec_count < 5 and r and recieve_data(ser,None):
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

def recieve_data(ser, _):
    data_r = ser.read(7)
    data_r = data_r.decode()
    data_r = float(data_r)
    if data_r <= 30:
        sen = True
    else:
        sen = False
    return sen

def transmit_data(ser, _):
    if _:
        data_t = '1'
    else:
        data_t = ''
    ser.write(str(data_t).encode())
    pass

if __name__ == '__main__':
    model_0 = YOLO('yolov8n-face.pt')
    model_1 = YOLO('best_btx.pt')

    ser = initialize_serial()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        r = human_detect(frame, model_0)
        # r = btx_detect(cap, model_1)
        # print(r)
        sen = recieve_data(ser,None)
        if r and b == False and sen:
            b = True
            run_thread(processing, arg1=cap, arg2=model_1, wait=False)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    ser.close()
