import sys
import telnetlib
import time
import Tkinter as tk
from tkMessageBox import *
from Application import *


#Requests input for Host and username

##HOST = raw_input("Enter your Host: ")
##user = raw_input("Enter username: ")
##server = raw_input("Enter your Server: ")
##folder = raw_input("Enter folder name: ")

app = Application(master=root)
app.mainloop()
print "in app"

HOST = app.HOST
user = app.user
server = app.server
folder = app.folder

print "from telnet " + HOST + user + server + folder
#+ server + folder
#print app.USB

reboot = "kill 1 1"
run = "/agk/bin/run"
mkdir = "mkdir /tmp/nvdmp"
mount_point = "fdisk -l|grep FAT|awk '{print $1}'"

time.sleep(20)

#Takes first telnet session and runs /agk/bin/run
def session():
    tn = telnetlib.Telnet(HOST)
    tn.set_debuglevel(1)
    tn.read_until("login: ")
    tn.write(user + "\n")
    return tn

tn1 = session()   
tn1.write("/agk/bin/run\n")
tn1.write("exit\n")

time.sleep(80)
tn2 = session()
tn2.write(reboot + "\n")
print tn2.read_all()
print "Reboot Now!"

time.sleep(220)

#3rd session to create directory and run
tn3 = session()
tn3.write(mkdir + "\n")
time.sleep(10)
if app.USB=="True":
    tn3.write("var=$(fdisk -l|grep FAT)\n")
    time.sleep(10)
    tn3.write("set -- $var\n")
    time.sleep(10)
    tn3.write("mount $1 /tmp/nvdmp\n")
else:
    tn3.write("mount -o,tcp,nolock " + server + ":/target/nvdumps/" + folder + " /tmp/nvdmp\n")
time.sleep(10)
tn3.write("export PATH=/bin:/usr/bin:/sbin:/usr/sbin\n")
time.sleep(10)
tn3.write("cat /tmp/nvdmp/nvram1.bin > /dev/nvram1\n")
time.sleep(10)
tn3.write("cat /tmp/nvdmp/nvram2.bin > /dev/nvram2\n")
time.sleep(10)
tn3.write("cat /tmp/nvdmp/backplane.bin > /dev/backplane\n")
time.sleep(10)
tn3.write("umount /nvram\n")
time.sleep(10)
tn3.write("mount -n -t nvram /nvram /nvram\n")
time.sleep(10)
tn3.write("rm -R /nvram/core/*\n")
time.sleep(10)
tn3.write("kill 1 1\n")
print tn3.read_all()
print "Reboot Now!"
if app.USB=="True":
    app.alert()
time.sleep(10)

time.sleep(350)

#4th session to delete */critical/* and bring game up
tn4 = session()
tn4.write("rm -R /nvram/permanent/critical/*\n")
tn4.write("rm -R /nvram/critical/*\n")
tn4.write(run + "\n")
tn4.write("exit\n")
print tn4.read_all()

