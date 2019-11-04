#Oct 29 2019
#Improvements
#Disable the ML feature to reenable once data is collected
#Incorperate logistic regression to predict in flow mental state
#Include random pop ups to collect data of "Yes" or "No" to question: In Flow?
#Disable buttons once activating 
#See if I can disable or shorten top bar of GUI
#clean up the layout of the GUI
   
#Make new layout functional
from tkinter import *
import tkinter as tk
import datetime as dt 
from datetime import timedelta
import os
import os.path
from os import path

from tkinter import messagebox as mb

from datetime import datetime

#import pandas as pd
#import numpy as np

import random
import itertools

#from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import GridSearchCV

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
    desiredHour.config(state="normal")
    desiredMin.config(state="normal")
    desiredSec.config(state="normal")
    BFTime.config(state="normal")
    BTdiff.config(state="normal")

def HideAllFun():
    swithcVal = CheckBoxVar.get()
    if swithcVal == 1:
        HeaderLabel.pack_forget()
        hlab.pack_forget()
        desiredHour.pack_forget()
        mlab.pack_forget()
        desiredMin.pack_forget()
        slab.pack_forget()
        desiredSec.pack_forget()
        BFTime.pack_forget()
        BTdiff.pack_forget()
    else:
        HeaderLabel.pack(side = LEFT)
        hlab.pack(side = LEFT)
        desiredHour.pack(side = LEFT)
        mlab.pack(side = LEFT)
        desiredMin.pack(side = LEFT)
        slab.pack(side = LEFT)
        desiredSec.pack(side = LEFT)
        BFTime.pack(side = LEFT)
        BTdiff.pack(side = LEFT)
        labelcurrTime.pack_forget()
        CountdownLabel.pack_forget()
    
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
    desiredHour.config(state="disable")
    desiredMin.config(state="disable")
    desiredSec.config(state="disable")
    BFTime.config(state="disable")
    BTdiff.config(state="disable")
    labelcurrTime.pack(side = LEFT)
    CountdownLabel.pack(side = LEFT)


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
    desiredHour.config(state="disable")
    desiredMin.config(state="disable")
    desiredSec.config(state="disable")
    BFTime.config(state="disable")
    BTdiff.config(state="disable")
    labelcurrTime.pack(side = LEFT)
    CountdownLabel.pack(side = LEFT)
    
def mState():
    test = mb.askyesno("Protool_V3", "Are You Focused?")
    if test is True:
        focusedFun(state = 1)
        #print(1)
    else:
        focusedFun(state = 0)
        #print(0)
    reseter.after(random.randint((30*60*1000), (45*60*1000)), mState)
    
def focusedFun(state):
    currentTime = dt.datetime.now()
    hour = str(currentTime.hour)
    minute = str(currentTime.minute)
    day = str(currentTime.day)
    month = str(currentTime.month)
    weekday = str(currentTime.weekday())
    state = str(state)
    
    if os.path.exists(PLpath) != True: 
        logFile= open(PLpath,"w+")
        logFile.write("hour,minute,day,month,weekday,state")
        logFile.write("\n")
        logFile.write(hour+","+minute+","+day+","+month+","+weekday+","+state)
        logFile.close() 
    else:
        logFile= open(PLpath,"a+")
        logFile.write("\n")
        logFile.write(hour+","+minute+","+day+","+month+","+weekday+","+state)
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
CheckBoxVar = IntVar()
colour = ["#0068a2", "#f1b310", "#e3481a", "#d90b27"]

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
CountdownLabel = Label(TopFrame)
hlab = Label(TopFrame, text="Hour:")
mlab = Label(TopFrame, text="Min:")
slab = Label(TopFrame, text="Sec:")
Spacer = Label(TopFrame, text=" ")
  
#Buttons
BFTime = tk.Button(TopFrame, text ="Future Time", command = GetFuture)
BTdiff = tk.Button(TopFrame, text ="Time Diff", command = GetTimeDiff)
reseter = tk.Button(TopFrame, text ="Reset", command = reset)
HideAllBox = Checkbutton(TopFrame, text="Hide", variable=CheckBoxVar, command = HideAllFun, offvalue=0, onvalue=1)
#HideAllBut = tk.Button(TopFrame, text ="Hide", command = HideAllFun)

#Text Box
ReasonBox = Text(TopFrame, height=1, width = 40)
ReasonBox.insert(INSERT, "")

#Canvas
Canvas = Canvas(TopFrame, width=(1440/2), height=20)

#App Layout
reseter.pack(side = LEFT)
HideAllBox.pack(side = LEFT)

HeaderLabel.pack(side = LEFT)

hlab.pack(side = LEFT)
desiredHour.pack(side = LEFT)
mlab.pack(side = LEFT)
desiredMin.pack(side = LEFT)
slab.pack(side = LEFT)
desiredSec.pack(side = LEFT)

BFTime.pack(side = LEFT)
BTdiff.pack(side = LEFT)

labelcurrTime.pack_forget()
CountdownLabel.pack_forget()

Canvas.pack_forget()

#Closing off of window function
mState()
root.minsize(350, 20)
root.wm_attributes("-topmost", 1)#Keep window on top of everything
root.title('Protool_V3 by Abul Hassan Sheikh')
root.mainloop()

