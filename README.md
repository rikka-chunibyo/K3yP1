# K3yP1
Raspberry Pi Zero and Arduino Pro Micro USB Hardware Keylogger

# Disclaimer
This is only as a Proof of Concept as a hobbyist I do not encourage anyone to use this tool for malicious purpose, that is not this repositories intention.

# How it works
This device works by sitting as a MITM between a USB keyboard and the computer it is meant to be connected to. It then logs the keystrokes that the user types.

The Keyboard is plugged into the Raspberry Pi which logs each character. This then passes the charcater over to the Arduino Pro Micro, using Serial communication, which is able to emulate the keystroke and therefore the keyboard will functionas normal.

## Things to be aware of
Certain control charcaters are not handled correctly although the most common ones are and if you need to add more control characters is should be fairly easy to work out how too by looking at the code and using [these](https://www.arduino.cc/en/Reference/KeyboardModifiers) charcater codes.

If the user types the esc key it will register it however it will only send the keystroke when another key is pressed.

## Requirements
- [5v Arduino Pro Micro](https://www.amazon.co.uk/KOOKYE-ATmega32U4-arduino-Leonardo-ATmega328/dp/B019SXN84E/ref=sr_1_1?s=computers&ie=UTF8&qid=1511045520&sr=1-1&keywords=arduino+pro+micro)
- [Raspberry Pi Zero with GPIO Header Pins](https://shop.pimoroni.com/products/raspberry-pi-zero)
- [Female to Female Jumper Cables](https://www.amazon.co.uk/Ganvol-Solderless-Flexible-Breadboard-Raspberry-Female/dp/B01LWAXJJS/ref=sr_1_4?s=computers&ie=UTF8&qid=1511045873&sr=1-4&keywords=female+to+female+jumper+cables)
- [Micro USB to USB Female adapter](https://www.amazon.co.uk/female-Micro-Adapter-Cable-Function/dp/B009DFCCKO/ref=sr_1_1?s=computers&ie=UTF8&qid=1511046003&sr=1-1&keywords=micro+usb+to+usb+female)
- [Micro USB to USB adapter](https://www.amazon.co.uk/Rankie-Braided-Extremely-Durable-Charging-Black/dp/B01JPEKJYI/ref=sr_1_6?ie=UTF8&qid=1511051894&sr=8-6&keywords=micro+usb+to+usb+male+cable)

You will also need a micro SD card for your Raspberry Pi Zero.

## Setup
Firstly you will want to image the lates version of Raspbian to your Raspberry Pi and set up SSH and USB Ethernet functionality. To do this you can follow [this](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/ethernet-gadget) tutorial. More information on flashin an SD card with an Operating system can be found [here](http://www.makeuseof.com/tag/install-operating-system-raspberry-pi/).

Now you should be able to SSH into the Raspberry Pi with the username ```pi``` and password ```raspberry```. From here we can begin to set up the Raspberry Pi to be able to capture Keystrokes.

The first thing you want to do is to Enable to serial port on the Raspberry Pi. To do this you can follow [this](http://hallard.me/enable-serial-port-on-raspberry-pi/) tutorial which tells you how to do it for both old and new verisons of Raspbian.

### Optional
This part of the setup is optional. If you want your Keylogger to be able to handle ctrl+alt+delete you will have to overwrite the ctrl+alt+delete system handler by creating your own service and running this when ctrl+alt+delete is pressed instead of the reboot service.

To do this first type ```sudo nano /etc/systemd/system/handlecad.service```. Now copy and paste the following into the file your editing
```
[Unit]
Description=Handle ctrl alt delete

[Service]
ExecStart=/bin/sh -c "sudo python /home/rikka/Pi-Keylogger/cad.py"

[Install]
WantedBy=multi-user.target
```
and save and exit.

Now type ``` sudo nano /lib/systemd/system/ctrl-alt-del.target``` and change the contents of the file too
```
[Unit]
Description=CTRL ALT DEL
Documentation=man:systemd.special(7)
DefaultDependencies=no
Requires=handlecad.service
After=handlecad.service
AllowIsolate=yes

[Install]
Alias=ctrl-alt-del.target
```


Now run the command ```sudo systemctl daemon-reload```.

Now the ctrl+alt+delete proccess should be overwritten and should run our servie ```handlecad.service``` which runs our file ```cad.py```.

### Setup continued
Now you will want to download this repository to your computer/laptop.

Now if you are not already logged into the Pi via SSH do so and run the command ```sudo mkdir /home/rikka/Pi-Keylogger```. Now run ```cd /home/pi/KeyP1```. This will take you to the directory you have just created. Now run ```sudo mkdir log```. Which should create a directory for you to store the log files.

Once this is all set up you will want to some how upload the two python files ```K3yP1.py, cad.py``` from this repository to the directory ```/home/rikka/Pi-Keylogger``` a simple way to do this is to use ```scp```. From a seperate terminal that is not logged into the Pi type ```sudo scp (file to transfer) pi@(ip address of the pi or .local name):K3yP1``` without brackets. Ths will then prompt you for a password and then transfer the file. Do this for both the K3ypi.py file and cad.py. It is important that both files are in the directory ```/home/rikka/Pi-Keylogger/```.

Now we must enable the Raspberry Pi to automatically login and then run a file. Therefore run the command ```sudo nano /etc/profile``` and at the very end of the file add ```sudo python /home/rikka/Pi-Keylogger/K3yP1.py```. This will automatically run our python file that captures keystrokes and logs them when the raspberry Pi logs in.

Now we must enable the Pi to automatically log in. [This](http://www.opentechguides.com/how-to/article/raspberry-pi/134/raspbian-jessie-autologin.html) tutorial demonstartes how to do this aswell as modifying ```/etc/profile``` to run a command/file of our choice. Once you have done this the Raspberry Pi setup is completed.

Once the Pi setup is complete we must flash the Arduino Pro micro with the ```keylogger.ino``` file using the Arduino IDE. Before you do this you will need to setup your IDE so it recognises the board if you have not worked with the Arduin Pro Micro before. To do this follow [this](https://learn.sparkfun.com/tutorials/pro-micro--fio-v3-hookup-guide) tutorial.

Once you have flashed the firware to your Arduino the last thing to do is to wire up the Arduino and Pi. To do this follow this wiring diagram.
```
Pi            Pro Micro    Colour
---------------------------------
5v             VCC          Red
GPIO14/TXD     RX           Yellow
GPIO15/RXD     TX           Yellow
GND            GND          Black
```
The Pinout of the Pro Micro can be found printed on its PCB whilst the pinout of the Raspberry Pi can be seen bellow.

![40 Pin Raspberry Pi pinout](http://i.imgur.com/CUgky6W.jpg)

Finally once you have everything setup plug your Micro USB to USB female into the Micro USB slot of the Pi that is used for both power and data it will be the one one the left if your looking at the pi with its header pins at the top.

Now when you plug your Keyboard into the USB female socket and plug your Arduino into the target computer with the Micro USB to USB adapter cable it will act as a hardware Keylogger. Then when you recover it it will have saved the keystrokes to a log file with the name as the date the log file was created.

## Be aware of
When you SSH back into the Pi after setting up the device or recovering it after logging keystrokes it will automatically run the Keylogger script. The escape key ist ctrl+e this will end the script and allow you to view your log files.

Although it is untested you may want to look into using ```sudo raspi-config``` and change the keyboard layouts of the Pi and see whether this changes how the keylogger replicates characters.

## Author
CuPcakeN1njA
