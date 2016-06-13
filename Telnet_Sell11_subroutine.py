import sys
import telnetlib
import time
from Tkinter import *
from tkMessageBox import *


#Requests input for Host and username

##HOST = raw_input("Enter your Host: ")
##user = raw_input("Enter username: ")
##server = raw_input("Enter your Server: ")
##folder = raw_input("Enter folder name: ")

class Application(Frame):
    fields = 'Host', 'User', 'Server', 'Folder'
    count = 0
    HOST = user = server = folder = ''
    
    def input_data(self):
        print "hi there, everyone!"

    def quitter(self):
        self.QUIT = Button(root)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.pack(side=RIGHT)


    def makeEntry(self, fields):
        entries = []
        for self.field in self.fields:
            self.row = Frame(root)
            self.lab = Label(self.row, width=5, text=self.field)            
            self.newentryname = StringVar()
            self.newentry = Entry(self.row, textvariable=self.newentryname)
            #self.newentry.insert(0, "Host")
            self.row.pack(side=TOP, fill=X)
            self.lab.pack(side=LEFT)
            self.newentry.pack(side=LEFT)
            entries.append(self.newentry)
        #self.createWidgets()
        return entries
       
    def reply(self):
        showinfo(title='Alert', message='Good to go!')        
        root.destroy()

    def fetch(self, entries):
        showinfo(title='Alert', message='Good to go!')
        for entry in entries:
            self.count = self.count + 1
##            print 'Input => %s' % entry.get()
##            print self.count
            if self.count == 1:
                self.HOST = entry.get()
            elif self.count == 2:self.user = entry.get()
            elif self.count == 3:self.server = entry.get()
            elif self.count == 4:
                self.folder = entry.get()
        root.destroy()
           
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        #top = self.top = Toplevel(hello)
        ents = self.makeEntry(self.fields)
        #master.bind('<Return>', (lambda event, e=ents: self.fetch(e)))
        Button(master, text='Submit',
               command=(lambda e=ents: self.fetch(e))).pack(side=LEFT)
        master.bind('<Return>', (lambda event, e=ents: self.fetch(e)))
        #master.bind('<Return>', self.quit)
        self.quitter()
        #Button(hello, text="Please Wait...", command=self.quit).pack()
        #Button(hello, text="Please Wait...", command=sys.exit).pack()
        #Quitter(root).pack(side=RIGHT)

root = Tk()
root.title('RDT')
app = Application(master=root)
app.mainloop()
#root.destroy()


HOST = app.HOST
user = app.user
server = app.server
folder = app.folder
print "from telnet " + HOST + user + server + folder

reboot = "kill 1 1"
run = "/agk/bin/run"
mkdir = "mkdir /tmp/nvdmp"

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
tn3.write("mount " + server + ":/target/nvdumps/" + folder + " /tmp/nvdmp\n")
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

time.sleep(350)

#4th session to delete */critical/* and bring game up
tn4 = session()
tn4.write("rm -R /nvram/permanent/critical/*\n")
tn4.write("rm -R /nvram/critical/*\n")
tn4.write(run + "\n")
tn4.write("exit\n")
print tn4.read_all()

