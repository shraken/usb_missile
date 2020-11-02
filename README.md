# USB Missile Launcher Tools

The USB Missile Launcher was a toy line of nerf-style USB controlled missile launch devices.  The devices
were manufactured by Dream Cheeky circa 2000's.  The missile launcher connects to a PC using a USB cable
and allows software control of rotation, elevation and fire command. 

There are several software binaries floating around to control the USB devices.  But compatability is
a problem.

This repo is a collection of tools to expand and enhance use.  These tools should run on
windows, linux, and macOS systems.  The tools are written in python and assume you are
using python3.    

## Supported Devices

Dream Cheeky seems like it was the original manufacturer for all of these devices.  Desklamations and
Brookstone look to be a re-brand based on the similarity of product photos but I can't say for certain
having not tested these devices.  The table below summarizes the different models.

| Device | Mfr | Tested |
| ----------- | ----------- | ----- |
| 908 Thunder Missile Launcher | Dream Cheeky | No |
| USB Desktop Missile Launcher | Brookstone | No |
| USB Circus Cannon | Dream Cheeky | No |
| USB Missile Launcher | Desklamations | No |
| Original Missile Launcher | Dream Cheeky | Yes |

## Software

| Script | Description |
| ------------ | ----------- |
| device.py    | HIDAPI interface to USB device |
| worker.py    | threading implementation for USB device control |
| gui.py       | tkinter GUI interface to expose rotate, elevation and fire control |
| interface.py | map inputs from gamepad to rotate, elevation, and fire control on USB device |

### Dependencies

The following python libraries are required when running these scripts:
 - [hidapi](https://pypi.org/project/hidapi/)
 - [inputs](https://pypi.org/project/inputs/)

```
pip install -r requirements.txt
```

## Usage

### GUI

Launch the graphical interface by running:

```shell
python src/gui.py
```

### Gamepad Interface

Launch the gamepad interface script by running:

```shell
python src/interface.py
```

## FAQ

1. Where can I buy one?

The units are no longer manufactured so eBay second-hand markets are best way to get one.

1. Where can I download binaries on my OS to run the GUI tool?

There are no download links available.  You must run the script with python and install are
required dependencies.  

1. 