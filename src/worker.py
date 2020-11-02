#!/usr/bin/python

'''
    Simple python thread to take inputs from a queue and execute movements or fire
     actions on missile launcher.
     
    10/31/2020
'''

import threading
import queue
import device as dc
import time

class Worker(threading.Thread):
    def __init__(self, q, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = q
        self.count = 0
        self.running = True
        self.device = None
        
        self.direction = ''
        self.active = False

        self.device = dc.init()
        if self.device == None:
            print('ERROR: could not initialize device, exiting..')

    def __del__(self):
        if self.device != None:
            if dc.exit(self.device) is False:
                print('ERROR: could not close device connection, exiting..')

    def decode(self, msg):
        if msg['status'] == 'stop':
            print('empty the queue now..')
            self.q.queue.clear()
            self.active = False
        elif msg['status'] == 'go':
            self.active = True
            self.direction = msg['motor']

    def process(self):
        if self.active:
            if self.direction == 'left':
                dc.rotateCCW(self.device)
            elif self.direction == 'right':
                dc.rotateCW(self.device)
            elif self.direction == 'up':
                dc.elevateUp(self.device)
            elif self.direction == 'down':
                dc.elevateDown(self.device)
            elif self.direction == 'fire':
                dc.fireMissile(self.device, 10.0)
                self.active = False

    def run(self):
        while self.running:
            # print('Thread running count = {}'.format(self.count))
            self.count += 1
            self.process()

            if not self.q.empty():
                print('queue not empty')
                item = self.q.get()
                print(item)
                if item:
                    self.decode(item)

            if self.q.empty():
                time.sleep(0.05)
        print('Thread exiting..')