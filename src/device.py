#!/usr/bin/python

'''
    Implement USB HIDAPI interface to Dream Cheeky line of USB controlled
     missile launchers.  

    10/29/2020
'''

import hid
import os
import time

# Dream Cheeky USB Missile Launcher vendor and product ID
USB_VID = 0x0A81
USB_PID = 0x0701

# constants
WRITE_VALUE = 0x01

# command to set mode
ROTATE_CW_CMD = 0x08
ROTATE_CCW_CMD = 0x04

ELEV_UP_CMD = 0x02
ELEV_DOWN_CMD = 0x01

FIRE_CMD = 0x10

# received status from device
STATUS_OK = 0x00
STATUS_LIMIT_ELEV_DOWN = 0x01
STATUS_LIMIT_ELEV_UP = 0x02
STATUS_LIMIT_ELEV = (STATUS_LIMIT_ELEV_UP | STATUS_LIMIT_ELEV_DOWN)

STATUS_LIMIT_ROTATE_CCW = 0x04
STATUS_LIMIT_ROTATE_CW = 0x08
STATUS_LIMIT_ROTATE = (STATUS_LIMIT_ROTATE_CCW | STATUS_LIMIT_ROTATE_CW)

STATUS_FIRE_DONE = 0x10

# continue command
CONTINUE_CMD = 0x40

# stop command
STOP_CMD = 0x20

def printStatus(status):
    if (status & STATUS_LIMIT_ELEV_DOWN):
        print('STATUS_LIMIT_ELEV_DOWN')
    elif (status & STATUS_LIMIT_ELEV_UP):
        print('STATUS_LIMIT_ELEV_UP')
    elif (status & STATUS_LIMIT_ROTATE_CCW):
        print('STATUS_LIMIT_ROTATE_CCW')
    elif (status & STATUS_LIMIT_ROTATE_CW):
        print('STATUS_LIMIT_ROTATE_CW')

def checkLimit(device, checkStatus):
    """
    Check if motor limit has been reached.  If the limit is found then
     a boolean False is returned.

    Args:
        device ([type]): object to USB hidapi
        checkStatus ([type]): device single byte return code bitmask value specifying
         if limit has been reached for motor.
    """
    d = device.read(1)
    if d:
        print(d)
        status = d[0]

        printStatus(status)
        if (checkStatus & status):
            return False
    return True

def execute(device, cmd, status, runTime):
    """
    Execute the command.  User specifies CW or CCW and time to run rotation.

    Args:
        device ([type]): [description]
        cmd ([type]): [description]
        status ([type]): status code to check against.  The device will issue
         these status if motor limit is encountered
        runTime ([type]): [description] motor time, if not supplied then
         optional 100 msec used.
    """
    device.write([WRITE_VALUE, cmd])
    startTime = time.time()
    while (time.time() - startTime) < runTime:
        device.write([WRITE_VALUE, CONTINUE_CMD])
        if checkLimit(device, status) == False:
            print('WARN execute check limit reached')
            break

    device.write([WRITE_VALUE, STOP_CMD])

def fireMissile(device, runTime = 0.1):
    """
    Fire ze missile.
    """
    device.write([WRITE_VALUE, FIRE_CMD])
    device.write([WRITE_VALUE, CONTINUE_CMD])
    time.sleep(0.01)

    # 7 runs, is this to pump?
    for _ in range(0, 7):
        device.write([WRITE_VALUE, FIRE_CMD])
        device.write([WRITE_VALUE, CONTINUE_CMD])
        device.write([WRITE_VALUE, CONTINUE_CMD])
        time.sleep(0.01)

    startTime = time.time()
    while (time.time() - startTime) < runTime:
        device.write([WRITE_VALUE, CONTINUE_CMD])
        d = device.read(1)
        if d:
            print(d)
            status = d[0]
            if status & STATUS_FIRE_DONE:
                print('fire status exit found')
                device.write([WRITE_VALUE, 0x20])
                break
        
        time.sleep(0.01)

    for _ in range(0, 10):
        device.write([WRITE_VALUE, CONTINUE_CMD])

def rotateCW(device, runTime = 0.1):
    """
    Rotate the launcher clockwise direction.
    """
    return execute(device, ROTATE_CCW_CMD, STATUS_LIMIT_ROTATE, runTime)

def rotateCCW(device, runTime = 0.1):
    """
    Rotate the launcher counter clockwise direction.
    """
    return execute(device, ROTATE_CW_CMD, STATUS_LIMIT_ROTATE, runTime)

def elevateUp(device, runTime = 0.1):
    """
    Elevate the launcher by moving UP direction.

    Args:
        device ([type]): [description]
        runTime ([type]): [description]
    """
    return execute(device, ELEV_UP_CMD, STATUS_LIMIT_ELEV_UP, runTime)

def elevateDown(device, runTime = 0.1):
    """
    Elevate the launcher by moving UP direction.

    Args:
        device ([type]): [description]
        runTime ([type]): [description]
    """
    return execute(device, ELEV_DOWN_CMD, STATUS_LIMIT_ELEV_DOWN, runTime)

def init():
    """
    Initialize USB connection to the device

    Returns:
        [type]: [description]
    """
    try:
        h = hid.device()
        h.open(USB_VID, USB_PID)
        h.set_nonblocking(1)
    except IOError as ex:
        print('ERROR: could not establish connection to device')
        print(ex)
        return None
    return h

def exit(h):
    """
    Close USB connection to device

    Args:
        h ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        h.close()
    except IOError as ex:
        print('ERROR: could not close hidapi device connection')
        print(ex)
        return False
    return True

def testMove():
    try:
        print("Opening the device")

        h = hid.device()
        h.open(USB_VID, USB_PID)

        print("Manufacturer: %s" % h.get_manufacturer_string())
        print("Product: %s" % h.get_product_string())
        print("Serial No: %s" % h.get_serial_number_string())

        # enable non-blocking mode
        h.set_nonblocking(1)

        # write some data to the device
        print("Rotate CW")
        rotateCW(h, 1.0)
        
        print("Rotate CCW")
        rotateCCW(h, 1.0)
        
        print("Elevate Up")
        elevateUp(h, 1.0)

        print("Elevate Down")
        elevateDown(h, 1.0)

        time.sleep(2)

        print("Closing the device")
        h.close()
    except IOError as ex:
        print(ex)
        print("You probably don't have the hard coded device. Update the hid.device line")
        print("in this script with one from the enumeration list output above and try again.")
    print("Done")

def testFire():
    try:
        print("Opening the device")

        h = hid.device()
        h.open(USB_VID, USB_PID)

        print("Manufacturer: %s" % h.get_manufacturer_string())
        print("Product: %s" % h.get_product_string())
        print("Serial No: %s" % h.get_serial_number_string())

        # enable non-blocking mode
        h.set_nonblocking(1)

        # here 
        fireMissile(h, 10.0)

        print("Closing the device")
        h.close()
    except IOError as ex:
        print(ex)
        print("You probably don't have the hard coded device. Update the hid.device line")
        print("in this script with one from the enumeration list output above and try again.")
    print("Done")

def listUsbHidDevices():
    """
    List attached USB HID devices
    """
    
    for d in hid.enumerate():
        keys = list(d.keys())
        keys.sort()
        for key in keys:
            print("%s : %s" % (key, d[key]))
        print()

if __name__ == "__main__":
    listUsbHidDevices()

    testMove()
    # testFire()