import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time
import RPi.GPIO as GPIO
from tkinter import *

#Var's to change
host = str("8.8.8.8")
timeOfflinetoReboot = 10           # Change this number to how many second with no ping before it reboots the kit
timeKitWithouPower = int(5)    # Change this number to how long you want the power shutoff to the kit during the reboot.

#Vars that don't need to be changed
sincereboot = int(20)     # This will need to be 420 later
offTime = int(0)
waittime = int(0)
running = str("yes")
reboots = int(0)
connectionEst = str('False')
timeToConnect = int(0)
firstDisconnect = 0
root = Tk()
root.title("Brian Cullen's Project")
root.geometry('500x450')
tf = Frame(root)
bf = Frame(root)
label_1 = Label(tf, text='\n' '       Press the button below to reboot the kit       ' '\n')
entry_log = Text(bf)

tf.pack()
bf.pack(side=BOTTOM)
label_1.pack()
entry_log.pack(fill=BOTH, expand=YES)

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

def reboot():
    GPIO.output(12, GPIO.HIGH)
    for i in range(timeKitWithouPower, 0, -1):
        printlog("Your device will be powered on in " + str(i) + " seconds", 'none')
        root.update()
        time.sleep(1)
    GPIO.output(12, GPIO.LOW)
    printlog("Your device has been rebooted and should be powering on now.", 'none')
    printlog('Your kit has been rebooted ' + str(reboots) + ' times.', 'warning')
    global connectionEst
    connectionEst = str('False')

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

def buttonReboot():
    printlog('You have clicked the reboot button', 'none')
    reboot()

def printlog(statement, state):
    print(str(statement))
    entry_log.config(state=NORMAL)
    entry_log.insert('1.0', str(statement) + '\n', str(state))
    entry_log.config(state=DISABLED)


def pauseScript():
    printlog('This button has not been programmed yet. Coming Soon.', 'none')


button1 = Button(tf, text='Reboot the kit', command=buttonReboot, height=3.5, width=30, bg='light blue')
button1.pack()
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label='File', menu=fileMenu)
fileMenu.add_command(label='Pause', command=pauseScript)
fileMenu.add_command(label='Exit', command=lambda: exit())
entry_log.tag_config('warning', background='yellow', foreground='red')
entry_log.tag_config('error', background='red', foreground='black')
entry_log.tag_config('good', foreground='green')
entry_log.tag_config('none', foreground='black')


while running == "yes":
    while connectionEst == 'False':
        if ping(host) == True:
            printlog('You are now connected and pinging will commence.', 'good')
            printlog('It took ' + str(timeToConnect) + ' seconds to establish a connection.', 'none')
            connectionEst = str('Connected')
            root.update()
            break
        else:
            if reboots == 0:
                printlog('Waiting ' + str(timeToConnect) + ' seconds for the initial connection to be established.', 'none')
                timeToConnect += 1
                time.sleep(1)
                if timeToConnect > 1200:  # this is time before it will reboot the kit on INITIAL startup.
                    printlog('Rebooting your device since it failed to establish a connection within 10 minutes', 'none')
                    reboot()
                root.update()
                continue
            else:
                printlog('Attempting to reestablish connection for ' + str(timeToConnect) + ' seconds.', 'none')
                timeToConnect += 1
                time.sleep(1)
                root.update()
                if timeToConnect > 600:  # This is time it will wait after a reboot before rebooting again.
                    printlog('Rebooting your device since it failed to establish a connection within 10 minutes', 'none')
                    reboot()
                continue
    while offTime > timeOfflinetoReboot:
        printlog("Your device is rebooting", 'none')
        reboot()
        reboots = reboots + 1
        printlog('Your device has been rebooted ' + str(reboots) + ' times.', 'none')
        connectionEst = str('False')
        offTime = 0
        root.update()
        break
    while waittime > 0:
        if waittime == 3:
            printlog("Waiting " + str(waittime) + " seconds to send another ping.", 'none')
        waittime = waittime - 1
        root.update()
        time.sleep(1)
        continue
    while waittime == 0:
        while ping(host) == True:
            printlog("You are Online", 'none')
            waittime= 3
            offTime= 0
            root.update()
            firstDisconnect = 0
            break
        else:
            if firstDisconnect < 1:
                printlog("You are now Offline", 'none')
            offTime= offTime + 10
            firstDisconnect += 1
            time.sleep(1)
            root.update()
            break
    continue
else:
    printlog('The program has crashed. Please contact Brian at (xxx) xxx-xxxx.', 'none')

printlog('The program has crashed. Please contact Brian at (xxx) xxx-xxxx.', 'none')

root.update()
