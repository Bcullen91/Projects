import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time
import RPi.GPIO as GPIO
from tkinter import *

host= str("8.8.8.8")  
sincereboot = int(20)     # This will need to be 420 later
offTime= int(0)         
waittime= int(0)         
running= str("yes")
reboots= int(0)
root = Tk()
root.geometry('500x500')


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

def reboot():
    GPIO.output(12, GPIO.HIGH)
    for i in range(10, 0, -1):
        print("Your device will be powered on in " + str(i) + " seconds")
        time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    print("Your device has been rebooted and should be powering on now.")
    global sincereboot
    sincereboot = 20

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

def buttonReboot():
    print('You have clicked the reboot button')
    global offTime
    offTime = offTime + 500

button1 = Button(root, text='Click here to Reboot the router', command=buttonReboot, height=450, width=450)
button1.pack()

while running == "yes":
    root.update()
    while sincereboot > 0:
        print("You will start pinging in " + str(sincereboot) + " seconds.")
        time.sleep(1)
        sincereboot = sincereboot - 1
        continue
    while offTime > 70:       # Will want to increase this later.
        global offTime
        global sincereboot
        print("Your device is rebooting")
        reboot()
        reboots = reboots + 1
        sincereboot = 40      # Will need to be 420 later
        offTime = 0
        break
    while waittime > 0:          
        print("Waiting " + str(waittime) + " seconds to send another ping.")
        time.sleep(1)
        waittime = waittime - 1
        continue
    while waittime == 0:           
        while ping(host) == True:
            print("You are Online")
            waittime= 3
            offTime= 0
            break
        else:           
            print("You are now Offline")
            offTime= offTime + 10
            print("You have been disconnected for " + str(offTime) + " seconds")
            time.sleep(1)
            break
    continue
else:
    print("Some error occurred and the the loop failed.")