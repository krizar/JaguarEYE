#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox
#import ttk
import tkinter
import configparser
import argparse
import datetime
#import imutils
import time
import logging
import threading 
import os 
import numpy as np
root = Tk()
root.attributes('-fullscreen', True)
# carga de archivo de configuracion
config = configparser.ConfigParser()
config.read("modos1.conf")
temamode = config.get("GENERAL","CDefault")
vgh = config.get(temamode,"vgh")
vgw = config.get(temamode,"vgw")
frt= config.get(temamode,"frt")
em =config.get(temamode,"em")
a =int(config.get(temamode,"a"))
ss =config.get(temamode,"ss")
vc = float(config.get(temamode,"vc"))
no1=str(config.get(temamode,"nom"))
r=int(config.get(temamode,"r"))
f=int(config.get(temamode,"f"))
nube=str(config.get(temamode,"nube"))
#  Termina carga de archivo

var1 = StringVar()
var1.set(temamode)
var2 = StringVar()
var2.set(frt)
var3 = StringVar()
var3.set(vgw)
var4 = StringVar()
var4.set(em)
var5 = StringVar()
var5.set(a)
var6 = StringVar()
var6.set(ss)
var7 = StringVar()
var7.set(int(vc))
var8 = StringVar()
var8.set(no1)
var9 = StringVar()
var9.set(r)
var10 = StringVar()
var10.set(f)
CheckVar1 = IntVar()
CheckVar1.set(nube)


C1 = Checkbutton(root, text = "nubes", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C1.pack()
parent = "false"
opt1 = OptionMenu(root, var1, 'FHD', 'HD', 'LD').pack(fill=X)
opt2 = OptionMenu(root, var2, '1', '2').pack(fill=X)
opt3 = OptionMenu(root, var3, '640X480', '1080X720').pack(fill=X)
opt4 = OptionMenu(root, var4, 'nube', 'No nube').pack(fill=X)
opt1 = OptionMenu(root, var5, 'FHD', 'HD', 'LD').pack(fill=X)
opt2 = OptionMenu(root, var6, '1', '2').pack(fill=X)
opt3 = OptionMenu(root, var7, '640X480', '1080X720').pack(fill=X)
opt4 = OptionMenu(root, var8, 'nube', 'No nube').pack(fill=X)
opt1 = OptionMenu(root, var9, 'FHD', 'HD', 'LD').pack(fill=X)
opt2 = OptionMenu(root, var10, '1', '2').pack(fill=X)
def state(): print(var1.get()) 


Button(root, command=state, text='Ver Lenguaje').pack()

root.mainloop()
#  



def main():
	
	return 0

if __name__ == '__main__':
	main()

