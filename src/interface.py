#!/usr/bin/python

'''
    Interface to allow a USB gamepad to control a USB missile launcher.  The
     movements and button actions on the gamepad are translated into commands
     for azimuth (rotation) and elevation directions on missile launcher.  

    10/31/2020
'''

import device as dc
import worker as worker
import inputs as inputs
from inputs import devices

import queue
import sys
import time
import signal
#from inputs import get_gamepad

class Interface:
    def __init__(self, q):
        self.running = True
        self.q = q

    def postMsg(self, status, motor):
        msg = {
            'status': status,
            'motor': motor,
        }
        self.q.put(msg)

    def process(self, event):
        print(event.ev_type, event.code, event.state)
        print(type(event.ev_type))
        if event.ev_type == 'Key':
            if (event.code == 'BTN_SOUTH') or \
               (event.code == 'BTN_TR'):
                if event.state == 1:
                    self.postMsg('go', 'fire')

        elif event.ev_type == 'Absolute':            
            if event.code == 'ABS_HAT0X':
                # direction pad rotate control
                if event.state == 1:
                    self.postMsg('go', 'left')
                elif event.state == -1:
                    self.postMsg('go', 'right')
                elif event.state == 0:
                    self.postMsg('stop', '')
            elif event.code == 'ABS_HAT0Y':
                # direction pad elevation control
                if event.state == 1:
                    self.postMsg('go', 'down')
                elif event.state == -1:
                    self.postMsg('go', 'up')
                elif event.state == 0:
                    self.postMsg('stop', '')
            elif event.code == 'ABS_X':
                # left stick button rotation control
                if event.state <= -1024:
                    self.postMsg('go', 'left')
                elif event.state >= 1024:
                    self.postMsg('go', 'right')
                elif ((event.state <= 128) and (event.state >= -128)):
                    self.postMsg('stop', '')
            elif event.code == 'ABS_Y':
                # left stick button elevation control
                if event.state <= -1024:
                    self.postMsg('go', 'down')
                elif event.state >= 1024:
                    self.postMsg('go', 'up')
                elif ((event.state <= 128) and (event.state >= -128)):
                    self.postMsg('stop', '')

    def exit(self):
        self.running = False

    def main(self):
        '''foo bar'''

        try:
            device = inputs.devices.gamepads[0]
        except IndexError:
            raise inputs.UnpluggedError("No gamepad found.")

        while self.running:
            #print('waiting start')
            # print(device)

            # this is a hack because python inputs only exposes blocking interface meant
            # to be iterated on.
            device._GamePad__check_state()
            events = device._do_iter()
            if events is None:
                continue

            for event in events:
                # print(event)
                self.process(event)

            #print('waiting done')
            time.sleep(0.05)
        print('wait loop exited')

q = queue.Queue()
intf = Interface(q)

def signal_handler(signal, frame):
    #print('You pressed Ctrl+C!')
    intf.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    print('USB Gamepad and Missile interface utility')
    
    thread = worker.Worker(q)
    thread.start()

    intf.main()
    print('main exited')
    intf.exit()

    thread.running = False
    thread.join()