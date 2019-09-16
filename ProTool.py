#Integrate text input 
   
#Make new layout functional
from tkinter import *
import tkinter as tk
import datetime as dt 
from datetime import timedelta
import os
import os.path
from os import path

#Make global variables
CDcontrol = True
CDvalueLeft = timedelta()
CDvalueTotal = timedelta()

#Get File Pating data
FilePath = os.path.abspath("ProTool.ipynb")
ParentPath = FilePath.split('ProTool.ipynb')[0]
PLpath = ParentPath+"ProductivityLog.csv"

#Pooled Functions
def reset():
    global CDcontrol
    CDcontrol = False
    CountdownLabel.configure(text='00:00:00')
    
def countdown(time):
    if not CDcontrol:
        return
    CountdownLabel['text'] = time
    
    global CDvalueLeft
    CDvalueLeft = time
    
    if time > timedelta(hours=0, minutes=0, seconds= 0):
        root.after(1000, countdown, time-timedelta(hours=0, minutes=0, seconds= 1))    
        
def GetFuture():
    global CDcontrol
    global CDvalueTotal
    CDcontrol = True
    currentTime = dt.datetime.now()
    CT_time = timedelta (hours=currentTime.hour, minutes=currentTime.minute, seconds= currentTime.second)
    dhour = int(desiredHour.get())
    dmin = int(desiredMin.get())
    dsec = int(desiredSec.get())
    DT_time = timedelta(hours=dhour, minutes=dmin, seconds= dsec)
    DiffValue = CT_time + DT_time 
    CDvalueTotal = DT_time
    countdown(time = DT_time)
    FT.set(DiffValue)



def GetTimeDiff():
    global CDcontrol
    global CDvalueTotal
    CDcontrol = True
    currentTime = dt.datetime.now()
    CT_time = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds= currentTime.second)
    dhour = int(desiredHour.get())
    dmin = int(desiredMin.get())
    dsec = int(desiredSec.get())
    DT_time = timedelta(hours=dhour, minutes=dmin, seconds= dsec)
    DiffValue =  DT_time - CT_time
    CDvalueTotal = DiffValue
    countdown(time = DiffValue)
    FT.set(DiffValue)
    
def distractedFun():
    currentTime = dt.datetime.now()
    Date = str(currentTime.year) + "-" + str(currentTime.month)+ "-" + str(currentTime.day)
    Weekday =  str(currentTime.isoweekday())
    Time = str(currentTime.hour) + ":" + str(currentTime.minute)

    typedData = ReasonBox.get("1.0",END)
    ReasonBox.delete("1.0",END)

    global CDvalueTotal, CDvalueLeft
    CDvalueCompleted = CDvalueTotal - CDvalueLeft
    
    if os.path.exists(PLpath) != True: 
        logFile= open(PLpath,"w+")
        logFile.write("Date, Weekday, Time, TotalTimer, TimerCompleted, TimerLeft, Status, Notes")
        logFile.write("\n")
        logFile.write(Date+","+ Weekday+","+ Time+","+str(CDvalueTotal)+","+str(CDvalueLeft)+","+str(CDvalueCompleted)+",Distracted,"+typedData)
        logFile.close() 
    else:
        logFile= open(PLpath,"a+")
        logFile.write(Date+","+ Weekday+","+ Time+","+str(CDvalueTotal)+","+str(CDvalueLeft)+","+str(CDvalueCompleted)+",Distracted,"+typedData)
        logFile.close() 

def focusedFun():
    currentTime = dt.datetime.now()
    Date = str(currentTime.year) + "-" + str(currentTime.month)+ "-" + str(currentTime.day)
    Weekday =  str(currentTime.isoweekday())
    Time = str(currentTime.hour) + ":" + str(currentTime.minute) 
    
    typedData = ReasonBox.get("1.0",END)
    ReasonBox.delete("1.0",END)

    global CDvalueTotal, CDvalueLeft
    CDvalueCompleted = CDvalueTotal - CDvalueLeft
    
    if os.path.exists(PLpath) != True: 
        logFile= open(PLpath,"w+")
        logFile.write("Date, Weekday, Time, TotalTimer, TimerCompleted, TimerLeft, Status, Notes")
        logFile.write("\n")
        logFile.write(Date+","+ Weekday+","+ Time+","+str(CDvalueTotal)+","+str(CDvalueLeft)+","+str(CDvalueCompleted)+",Focused,"+typedData)
        logFile.close() 
    else:
        logFile= open(PLpath,"a+")
        logFile.write(Date+","+ Weekday+","+ Time+","+str(CDvalueTotal)+","+str(CDvalueLeft)+","+str(CDvalueCompleted)+",Focused,"+typedData)
        logFile.close()    
    

#Dummy Print function to test out Distraction/focused buttons
def DummyFun():
    currentTime = dt.datetime.now()
    Date = str(currentTime.year) + "-" + str(currentTime.month)+ "-" + str(currentTime.day)
    Weekday =  str(currentTime.isoweekday())
    Time = str(currentTime.hour) + ":" + str(currentTime.minute) 
    typedData = ReasonBox.get("1.0",END)
    ReasonBox.delete("1.0",END)
    global CDvalueTotal, CDvalueLeft
    CDvalueCompleted = CDvalueTotal - CDvalueLeft
    print(Date+","+ Weekday+","+ Time+","+str(CDvalueTotal)+","+str(CDvalueLeft)+","+str(CDvalueCompleted)+","+typedData)
    
    
#Windowing function 
root = Tk()
FT = StringVar()
logText = StringVar()


#Make the frames
TopFrame = Frame(root)
TopFrame.pack()

desiredHour = Spinbox(TopFrame, from_=0, to=23, width = 2)
desiredMin = Spinbox(TopFrame, from_=0, to=59, width = 2)
desiredSec = Spinbox(TopFrame, from_=0, to=59, width = 2)

dhour = int(desiredHour.get())
dmin = int(desiredMin.get())
dsec = int(desiredSec.get())

#labels
HeaderLabel = Label(TopFrame, text="Calculation Modes:")
labelcurrTime = Label( TopFrame, textvariable=FT)
CountdownLabel = Label(TopFrame, text='00:00:00')
hlab = Label(TopFrame, text="Hour:")
mlab = Label(TopFrame, text="Min:")
slab = Label(TopFrame, text="Sec:")
Spacer = Label(TopFrame, text=" ", background='light gray')
  
#Buttons
BFTime = tk.Button(TopFrame, text ="Future Time", command = GetFuture)
BTdiff = tk.Button(TopFrame, text ="Time Diff", command = GetTimeDiff)
reseter = tk.Button(TopFrame, text ="reset", command = reset)
DistractedBut = tk.Button(TopFrame, text ="Distracted", command = distractedFun)
FocusedBut = tk.Button(TopFrame, text ="Focused", command = focusedFun)

#Text Box
ReasonBox = Text(TopFrame, height=1, width = 40)
ReasonBox.insert(INSERT, "")

#App Layout
reseter.pack(side = LEFT)

HeaderLabel.pack(side = LEFT)

Spacer.pack(side = LEFT)

hlab.pack(side = LEFT)
desiredHour.pack(side = LEFT)
mlab.pack(side = LEFT)
desiredMin.pack(side = LEFT)
slab.pack(side = LEFT)
desiredSec.pack(side = LEFT)

Spacer.pack(side = LEFT)

BFTime.pack(side = LEFT)
BTdiff.pack(side = LEFT)

Spacer.pack(side = LEFT)

labelcurrTime.pack(side = LEFT)
CountdownLabel.pack(side = LEFT)

Spacer.pack(side = LEFT)

DistractedBut.pack(side = LEFT)
FocusedBut.pack(side = LEFT)


ReasonBox.pack(side = LEFT)
#Closing off of window function
label = Label(root)
root.wm_attributes("-topmost", 1)#Keep window on top of everything
root.iconbitmap(r'\\TDOTFS01\Group\Data Team\Abul\1. Code\O1_P1_ProTool\O1_P1_ProTool_PR_S_icon.ico')
root.title('Protool_V2 by Abul Hassan Sheikh')
root.mainloop()

