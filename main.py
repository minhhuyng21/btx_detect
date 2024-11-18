import tkinter as tk
from ultralytics import YOLO
import cv2
import json
def btx_detect_rt(frame, model):
    results = model.predict(source=frame , conf=0.6)
    a_frame = results[0].plot()
    # json_str = results[0].tojson()
    # json_list = json.loads(json_str)
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('AI-BTX',a_frame)
    # if len(json_list) >= 1:
    #     return True
    # return False

if __name__ == '__main__':
    # model_0 = YOLO('yolov8n0face.pt')
    model_1 = YOLO('model/best_btx.pt')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        r = btx_detect_rt(frame, model_1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# def my_function():
# # Hàm riêng của bạn được gọi khi click nút "Start"
#     print("Hàm riêng được thực thi!")
#     detect()

# # Khởi tạo Tkinter
# window = tk.Tk()

# # Cài đặt tiêu đề cho cửa sổ
# window.title("Ứng dụng Tkinter cơ bản")
# # Tạo khung chứa giao diện
# frame = tk.Frame(window,background="")
# frame.pack()

# label = tk.Label(frame, text="Welcome to Bui Thi Xuan detection",font=('Arial',20))
# label.pack()

# # Tạo nút "Start"
# start_button = tk.Button(frame, text="Start",font=('Arial',20), command=my_function,background='blue')
# start_button.pack()
# window.geometry("600x400")
# # Chạy vòng lặp chính để hiển thị giao diện
# window.mainloop()