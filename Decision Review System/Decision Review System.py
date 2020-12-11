import tkinter # This is an in-built package
import PIL.Image, PIL.ImageTk # pip install pillow
import cv2 # pip install opencv-python
from functools import partial # partial puts the argument into the function, but to the command it
                                # seems like there is no argument into the function.
import threading # to avoid the blocking nature of program we use 'threading.'
import imutils
import time

stream = cv2.VideoCapture('clip.mp4')
flag = True

def play(speed):
    global flag
    print(f'You clicked on play. The speed is {speed}.')
    
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES) # This is the variable which stores which frame are you rading.
    stream.set(cv2.CAP_PROP_POS_FRAMES, speed + frame1) 

    grabbed, frame = stream.read() # grabbed tells us if the frame selected is correct or not.
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    if flag:
        canvas.create_text(250, 20, fill='black', font='Times 27 bold', text='Decision Pending')
    flag = not flag

def pending(decision):
    # 1. Display Decision Pending Image
    frame = cv2.cvtColor(cv2.imread('pending.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame) 
    # 2. Wait for 1 second
    time.sleep(1)
    # 3. Display Sponsor Image
    frame = cv2.cvtColor(cv2.imread('sponsor.png'), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)
    # 4. Wait for 1.5 second
    time.sleep(1.5)
    # 5. Display Out/Not Out Image
    if decision == 'out':
        decisionImg = 'out.png'
    else:
        decisionImg = 'not_out.png'
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, anchor=tkinter.NW, image=frame)

    

def out():
    thread = threading.Thread(target=pending, args=('out',))
    thread.daemon = 1
    thread.start()
    print('The player is Out.')

def not_out():
    thread = threading.Thread(target=pending, args=('not out',))
    thread.daemon = 1
    thread.start()
    print('The player is Not Out.')
# width and height of the mainscreen
SET_WIDTH = 650
SET_HEIGHT = 368

# tkinter GUI starts here..
window = tkinter.Tk() # It'll create the tkinter window
window.title('Nothing_Wrong Decision Review System')

cv_img = cv2.cvtColor(cv2.imread('sponsor.png'), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
# To put a png image into the canvas we use the followig code.
# we're using fromarray, 'coz we'll use opencv and read the image in the form of array.
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
# here cv_img is an opencv image.
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

btn = tkinter.Button(window, text='<< previous (fast)', width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text='<< previous (slow)', width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text='next (fast) >>', width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text='next (slow) >>', width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text='Give Out', width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text='Give Not Out', width=50, command=not_out)
btn.pack()

window.mainloop()