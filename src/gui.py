#!/usr/bin/python

'''
    Control USB Missile Launcher using basic GUI.  The GUI allows the
     elevation and azmith angle of the launcher to be set by clicking the
     directional up, down, left and right buttons.  The user clicks the
     center fire button to launch a missile.  

    10/29/2020
'''

from tkinter import *
import time
import threading
import worker as worker
import queue

q = queue.Queue()
neutral_color = 'SystemButtonFace'
active_color = 'snow3'
button_color = 'lightgray'

def postMsg(status, motor):
    msg = {
        'status': status,
        'motor': motor,
    }
    q.put(msg)

# up arrow
def pressUp(event):
    return postMsg('go', 'up')

def releaseUp(event):
    return postMsg('stop', 'up')

# down arrow
def pressDown(event):
    return postMsg('go', 'down')

def releaseDown(event):
    return postMsg('stop', 'down')

# left arrow
def pressLeft(event):
    return postMsg('go', 'left')

def releaseLeft(event):
    return postMsg('stop', 'left')

# right arrow
def pressRight(event):
    return postMsg('go', 'right')

def releaseRight(event):
    return postMsg('stop', 'right')

# fire
def pressFire(event):
    return postMsg('go', 'fire')

# GUI definitions
root = Tk()
root.title('USB Missile Controller')
root.resizable(width=False, height=False)
root.geometry('+550+100')
root.geometry('600x480')
root.configure(bg=neutral_color)

# images for buttons in gamefield
up_picture = PhotoImage(file='graphics/up.png')
down_picture = PhotoImage(file='graphics/down.png')
left_picture = PhotoImage(file='graphics/left.png')
right_picture = PhotoImage(file='graphics/right.png')
fire_picture = PhotoImage(file='graphics/fire.png')

# Row 1
ButtonRow1 = Frame(root, bg=neutral_color)
ButtonRow1.config(borderwidth=0, relief=FLAT)

ButtonUp = Button(ButtonRow1, bg=button_color, activebackground=active_color, 
                  height=150, width=150)
ButtonUp.pack(side=LEFT)
ButtonUp.bind('<ButtonPress-1>', pressUp)
ButtonUp.bind('<ButtonRelease-1>', releaseUp)

ButtonUp.config(image=up_picture)
ButtonRow1.pack(side=TOP, expand=1)

# Row2
ButtonRow2 = Frame(root, bg=neutral_color)
ButtonRow2.config(borderwidth=0, relief=FLAT)

ButtonLeft = Button(ButtonRow2, bg=button_color, activebackground=active_color, 
                    height=150, width=150)
ButtonLeft.pack(side=LEFT)
ButtonLeft.bind('<ButtonPress-1>', pressLeft)
ButtonLeft.bind('<ButtonRelease-1>', releaseLeft)

ButtonLeft.config(image=left_picture)

ButtonFire = Button(ButtonRow2, bg=button_color, activebackground=active_color, 
                    height=150, width=150)
ButtonFire.pack(side=LEFT)
ButtonFire.config(image=fire_picture)
ButtonFire.bind('<ButtonPress-1>', pressFire)

ButtonRight = Button(ButtonRow2, bg=button_color, activebackground=active_color, 
                     height=150, width=150)
ButtonRight.pack(side=LEFT)
ButtonRight.bind('<ButtonPress-1>', pressRight)
ButtonRight.bind('<ButtonRelease-1>', releaseRight)

ButtonRight.config(image=right_picture)
ButtonRow2.pack(side=TOP, expand=1)

# Row 3
ButtonRow3 = Frame(root, bg=neutral_color)
ButtonRow3.config(borderwidth=0, relief=FLAT)

ButtonDown = Button(ButtonRow3, bg=button_color, activebackground=active_color, 
                    height=150, width=150)
ButtonDown.pack(side=LEFT)
ButtonDown.config(image=down_picture)
ButtonDown.bind('<ButtonPress-1>', pressDown)
ButtonDown.bind('<ButtonRelease-1>', releaseDown)

ButtonRow3.pack(side=TOP, expand=1)

thread = worker.Worker(q)
thread.start()

root.mainloop()

thread.running = False
thread.join()