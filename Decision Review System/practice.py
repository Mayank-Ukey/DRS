import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import time
import imutils

stream = cv2.VideoCapture("clip.mp4")
flag = True
def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tk.NW, image=frame)
    if flag:
        canvas.create_text(120, 20, fill="white", font="Times 27 bold", text="Decision Pending")
    flag = not flag

def pending(decision):
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tk.NW, image=frame)
    time.sleep(1)

    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tk.NW, image=frame)
    time.sleep(1.5)

    if decision=="out":
        frame = cv2.cvtColor(cv2.imread("out.png"), cv2.COLOR_BGR2RGB)
    else:
        frame = cv2.cvtColor(cv2.imread("not_out.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tk.NW, image=frame)

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
SET_WIDTH = 650
SET_HEIGHT = 368
window = tk.Tk()
window.title("Mayank Ukey Decision Review System")

cv_img = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
canvas = tk.Canvas(window, width=SET_WIDTH, height= SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.pack()

btn = tk.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tk.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tk.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tk.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tk.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tk.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()
window.mainloop()