import tkinter
import cv2
import PIL.ImageTk, PIL.Image
from functools import partial
import threading 
import time
import imutils

stream = cv2.VideoCapture('clip.mp4')
flag = True 

def play(speed):
    global flag
    print(f'You clicked play, the speed is {speed}.')
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    if flag:
        canvas.create_text(250, 50, fill='red', font='Times 27 bold', text='Decision Pending')
    flag = not flag 

def pending(decision):
    frame = cv2.cvtColor(cv2.imread('pending.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image= frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    time.sleep(1)

    frame = cv2.cvtColor(cv2.imread('sponsor.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.Photoimage(image=PIL.Image.fromarray(frame))
    canvas.image=frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    time.sleep(1.5)

    if decision=='out':
        decisionImg = 'out.png'
    else:
        decisionImg = 'not_out.png'

    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image= frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)


def out():
    thread = threading.Thread(target=pending, args=('out',))
    thread.daemon = 1
    thread.start()
    print('The player is out.')

def not_out():
    thread = threading.Thread(target=pending, args=('not_out',))
    thread.daemon=1
    thread.start()
    print('The player is not out.')

SET_WIDTH = 650
SET_HEIGHT= 368

window = tkinter.Tk()
window.title('Nothing Wrong Decision Review System')

cv_img = cv2.cvtColor(cv2.imread('sponsor.png'), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

btn = tkinter.Button(window, text='<< previous (fast)', width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text='<< previous (slow)', width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text='next (fast) >>', width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text = 'next (slow) >>', width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text='Give Out', width = 50, command=out)
btn.pack()

btn = tkinter.Button(window, text='Give Not Out', width=50, command=not_out)
btn.pack()

window.mainloop()