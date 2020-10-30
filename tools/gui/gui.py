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

neutral_color = 'SystemButtonFace'
active_color = 'snow3'
button_color = 'lightgray'

def pressUp(event):
    print('pressUp')
    pass

def releaseUp(event):
    print('releaseUp')
    pass

def InfiniteProcess():
    while not finish:
        print("Infinite Loop")
        time.sleep(3)

finish = False

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
                    height=150, width=150, command=lambda: buttonPushed(ButtonLeft))
ButtonLeft.pack(side=LEFT)
ButtonLeft.config(image=left_picture)

ButtonFire = Button(ButtonRow2, bg=button_color, activebackground=active_color, 
                    height=150, width=150, command=lambda: buttonPushed(ButtonFire))
ButtonFire.pack(side=LEFT)
ButtonFire.config(image=fire_picture)

ButtonRight = Button(ButtonRow2, bg=button_color, activebackground=active_color, 
                     height=150, width=150, command=lambda: buttonPushed(ButtonRight))
ButtonRight.pack(side=LEFT)
ButtonRight.config(image=right_picture)

ButtonRow2.pack(side=TOP, expand=1)

# Row 3
ButtonRow3 = Frame(root, bg=neutral_color)
ButtonRow3.config(borderwidth=0, relief=FLAT)

ButtonDown = Button(ButtonRow3, bg=button_color, activebackground=active_color, 
                    height=150, width=150, command=lambda: buttonPushed(ButtonDown))
ButtonDown.pack(side=LEFT)
ButtonDown.config(image=down_picture)

ButtonRow3.pack(side=TOP, expand=1)

Process = threading.Thread(target=InfiniteProcess)
Process.start()

root.mainloop()
finish = True
Process.join()