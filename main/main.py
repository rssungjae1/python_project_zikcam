import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
from tkinter import filedialog # 서브모듈이라서 별도로 import
from PIL import Image
from cv2 import cv2
import numpy as np

root = Tk()
root.title("SONG ZikCAM")

# 파일 추가 기능
def add_file():
    global file
    file = filedialog.askopenfilename(title="동영상 파일을 선택하세요", \
        filetypes=[("mp4 파일","*.mp4")],\
        initialdir=r"main\videos") 
        # 최초에 사용자가 지정한 경로를 보여줌

    # 사용자가 선택한 파일 목록 출력
    entry_file.insert(END, file)

# 선택 삭제 기능
def del_file():
    entry_file.delete(0,"end")

# 저장 경로 (폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory(initialdir=r"main\video_result")
    if folder_selected == '': # 사용자가 취소를 누를때
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# 시작
def start():
    # 파일 목록 확인
    if entry_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return
    # 저장 경로 확인
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return
    zikcam(file)
    
def zikcam(video_path):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, float(start_frame_entry.get()))

    if not cap.isOpened():
        exit()

    tracker = cv2.TrackerCSRT_create()
    # tracker 종류
    # https://rosia.tistory.com/243
    # cv2.TrackerCSRT_create()
    # cv2.TrackerKCF_create()
    # cv2.TrackerMOSSE_create()
    # cv2.TrackerMIL_create()
    # cv2.TrackerBoosting_create()
    # cv2.TrackerMedianFlow_create()
    # cv2.TrackerTLD_create()
    # cv2.TrackerGOTURN_create()
    
    # 프레임 읽어주기
    rect, img = cap.read()
    cv2.namedWindow('Select Window')
    cv2.imshow('Select Window', img)
    output_size = (300 , 700)
    # initialize writing video
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get
    (cv2.CAP_PROP_FPS), output_size)

    # setting ROI
    rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow('Select Window')

    # initialize tracker
    tracker.init(img, rect)

    while True:
        ret,img = cap.read()
        print(cap.get(cv2.CAP_PROP_POS_FRAMES))
        
        print(float(end_frame_entry.get()))
        if float(end_frame_entry.get()) == cap.get(cv2.CAP_PROP_POS_FRAMES):
            exit()
        if not ret:
            exit()
        success, box = tracker.update(img)
        left, top, w, h = [int(v) for v in box]
        
        center_x = left + w /2 
        center_y = top + h /2

        result_top = int(center_y - output_size[1] /3)
        result_bottom = int(center_y + output_size[1] /3 *2)
        result_left = int(center_x - output_size[0] /2)
        result_right = int(center_x + output_size[0] /2)

        result_img = img[result_top:result_bottom, result_left:result_right].copy()

        out.write(result_img)
        cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255,255,255), thickness=3)

        cv2.imshow('result_img', result_img)
        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            break

# 파일 프레임
file_frame = Frame(root)
file_frame.pack(fill="both", padx=5, pady=5)

btn1 = Button(file_frame, text="파일추가", padx=5, pady=5, width=12, command=add_file)
btn1.pack(side="left")
btn2 = Button(file_frame, text="삭제", padx=5, pady=5, width=12, command=del_file)
btn2.pack(side="right")

#  해당 프레임
entry_frame = Frame(root)
entry_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(entry_frame, orient=HORIZONTAL)
scrollbar.pack(side="bottom", fill="x")

entry_file = Entry(entry_frame, xscrollcommand=scrollbar.set)
entry_file.pack(side="bottom", fill="both", expand=True)
scrollbar.config(command=entry_file.xview)

# 저장 경로 프레임
path_frame = LabelFrame(root, text="저장경로")
path_frame.pack(fill="both", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 옵션 프레임
frame_option = LabelFrame(root, text="옵션")
frame_option.pack(padx=5, pady=5, ipady=5)

# 1. 시작 프레임
start_frame = Label(frame_option, text="시작 프레임", width=8)
start_frame.pack(side="left", padx=5, pady=5)
start_frame_entry = ttk.Entry(frame_option)
start_frame_entry.pack(side="left", padx=5, pady=5)

# 2. 종료 프레임
end_frame = Label(frame_option, text="종료 프레임", width=8)
end_frame.pack(side="left", padx=5, pady=5)
end_frame_entry = ttk.Entry(frame_option)
end_frame_entry.pack(side="left", padx=5, pady=5)

# 사용 설명 프레임
howto = LabelFrame(root, text="사용설명")
howto.pack(padx=5, pady=5, ipady=5, fill="both")
howto_frame = Label(howto,  justify ="left",
    text="파일형식 - .mp4 \n 시작 프레임 - 영역 선택 프레임(숫자) \n 종료 프레임 - 직캠 종료 프레임(숫자) \n\n 프로그램 작동 흐름 \
    \n 시작 - 첫 시작 프레임 - 마우스 왼쪽클릭으로 영역 지정- space선택 - 종료를 원하면 'q'버튼")
howto_frame.pack(side="left", padx=5, pady=5)


# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()