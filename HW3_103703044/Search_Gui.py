#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from matplotlib import *

import pickle

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog 
from ttk import Frame, Button, Label, Style
import numpy as np
from random import randint
from PIL import Image
import math
import Q1
import Q2
import Q3
import Q4

global imgs
global thumb
global baseImage
global fileList
global fileName
class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    
        
    def initUI(self):
        #title
        self.parent.title("HW3") 
        #pack_info
        self.pack(fill=BOTH, expand=1)
        #Button_SelectFile
        Button(self, text = "Select File", command = openFile).grid(row=0, column=0, pady=5)
        self.fileName = StringVar()
        Label(self, textvariable=self.fileName).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

        #Default_file
        self.fileName = StringVar(value = "./dataset/ukbench00000.jpg")

        #Image_SelectedFile
        self.thumb = Label(self)
        self.thumb.grid(row=0, column=1, pady=5, sticky=W)
        image = Image.open(self.fileName.get())
        image = ImageTk.PhotoImage(image.resize((int(image.size[0]*0.8), int(image.size[1]*0.8)),Image.ANTIALIAS))
        self.thumb.configure(image = image)
        self.thumb.image = image

        #mode_SelectMode
        Label(self, text = "Select Mode: ").grid(row=1, column=0, pady=5)
        mode = StringVar(self)
        #default
        mode.set("Q3-SIFT Visual Words")
        om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words")
        om.grid(row=1, column=1, pady=5, sticky=W)

        #Button_Search
        Button(self, text = "SEARCH", command = lambda: startSearching(self.fileName.get(),mode.get())).grid(row=3, column=0, pady=5)
        self.imgs = []
        #RankList
        for i in xrange(10):
            self.imgs.append(Label(self))
            self.imgs[i].grid(row=i/5+4, column=i%5, padx=5, pady=10)
 
def openFile ():
    fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
    app.fileName.set(fileName)
    image = Image.open(app.fileName.get())
    image = ImageTk.PhotoImage(image.resize((int(image.size[0]*0.8), int(image.size[1]*0.8)),Image.ANTIALIAS))
    app.thumb.configure(image = image)
    app.thumb.image = image

def startSearching (fileName, mode):
    baseImage = Image.open(fileName)
    fileList = os.listdir(fileName[:-16])
    fileName = fileName[-16:]
    if mode == "Q1-ColorHistogram":
        rank = Q1.Q1_run(baseImage,fileList)
  
    elif mode == "Q2-ColorLayout":
        if os.path.exists("./offline/Q2_DCTData.csv"):
            rank = Q2.Q2_offline_run(fileName,fileList)
        else:
            rank = Q2.Q2_run(baseImage,fileList)


    elif mode == "Q3-SIFT Visual Words":
    	if os.path.exists("./offline/Q3.csv"):
            rank = Q3.Q3_offline_run(fileName,fileList)
    elif mode == "Q4-Visual Words using stop words":
        if os.path.exists("./offline/Q3.csv"):
            rank = Q4.Q4_offline_run(fileName,fileList)

    for i in xrange(10):
        imgName = "./dataset/" + rank[i][1]
        image = Image.open(imgName)
        image = ImageTk.PhotoImage(image.resize((int(image.size[0]*0.8), int(image.size[1]*0.8)),Image.ANTIALIAS))
        app.imgs[i].configure(image = image)
        app.imgs[i].image = image
        print "Rank " + str(i+1) + " is number " + rank[i][1][7:-4] + ", distance is " + str(round(rank[i][0],3))

if __name__ == '__main__':
    root = Tk()
    size = 220, 220
    app = Example(root)
    root.geometry("1000x800")
    root.mainloop()
 

  