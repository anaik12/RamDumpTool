import sys
import telnetlib
import time
import Tkinter as tk
from tkMessageBox import *

#USB=True
#Exit=False
class Application(tk.Frame):
    fields = 'Host', 'User', 'Server', 'Folder'
    count = 0
    HOST = user = server = folder = ''
    USB = "False"
    #Exit = "False"
    #USB = "{0}".format(var.get())
    #var = tk.BooleanVar()
    
    def input_data(self):
        print "hi there, everyone!"

    def quitter(self):
        #self.Exit = "True"
        self.QUIT = tk.Button(root)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = root.destroy
        self.QUIT.pack(side=tk.RIGHT)


    def makeEntry(self, fields, var):
        entries = []
        for self.field in self.fields:
            self.row = tk.Frame(root)
            self.lab = tk.Label(self.row, width=5, text=self.field)            
            self.newentryname = tk.StringVar()
            self.newentry = tk.Entry(self.row, textvariable=self.newentryname)
            #else: self.newentry = tk.Entry(self.row, textvariable=self.newentryname)
            self.row.pack(side=tk.TOP, fill=tk.X)
            #self.row.focus_set()
            self.lab.pack(side=tk.LEFT)
            self.newentry.pack(side=tk.LEFT)
            #self.newentry.bg="red"
            entries.append(self.newentry)
            #if (self.USB==True and self.newentryname in ['Server','Folder']):           
        return entries
       
    def reply(self):
        showinfo(title='Alert', message='Good to go!')        
        root.destroy()

    def alert(self):
        #root.withdraw()
        showinfo(title='Alert', message='Disconnect USB!')
        root.destroy()

    def fetch(self, entries):
        showinfo(title='Alert', message='Good to go!')
        for entry in entries:
            self.count = self.count + 1
            if self.count == 1:self.HOST = entry.get()
            elif self.count == 2:self.user = entry.get()
            elif self.count == 3:self.server = entry.get()
            elif self.count == 4:
                self.folder = entry.get()
        #root.destroy()
        root.withdraw()
        root.quit()
        #self.quit
   
    def check(self, entries):
        #states[i]= not states[i]
        #USB = not USB
        self.USB = "{0}".format(var.get())
        for index, entry in enumerate(entries):
            if index < 2: continue
            else:
                if var.get():
                    entry.configure(state=tk.DISABLED)
                else: entry.configure(state=tk.NORMAL)
                #print USB
                #print "variable is {0}".format(var.get())
        return
        
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        #top = self.top = Toplevel(hello)
        ents = self.makeEntry(self.fields, var)        
        tk.Button(root, text='Submit',
               command=(lambda e=ents: self.fetch(e))).pack(side=tk.LEFT)
        root.bind('<Return>', (lambda event, e=ents: self.fetch(e)))
                
        chk = tk.Checkbutton(root, text="USB", variable=var, command=(lambda e=ents: self.check(e)))
        chk.pack(side=tk.LEFT, anchor=tk.N, expand=NO)        
        #master.bind('<Return>', (lambda event, e=ents: self.fetch(e)))  
        self.quitter()           

root = tk.Tk()
root.title('RDT')
#root.update_idletasks()
var = tk.BooleanVar()
#root.mainloop()
#root.update()
