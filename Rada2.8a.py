import cv2
import picamera
import picamera.array
import argparse
import datetime
#import imutils
import time
import logging
import threading 
import os 
import numpy as np
def nom(z):
    ahora = datetime.datetime.now()
    fech = ahora.strftime("%d%m%y%H%M%S")
    z = z + str(fech)
    return z
def reloj(x):
    ahora = datetime.datetime.now()
    tiempo = ahora + datetime.timedelta(seconds=int(x))
    return tiempo
def cronometro(y):
    tp1 = datetime.datetime.now()
    ts1 = int(tp1.strftime("%d%m%y%H%M%S%f")) - int(y.strftime("%d%m%y%H%M%S%f"))
    return str(ts1)
def fotocap(xfoto, carpeta1, frame, iden):
    x1foto = iden + str(xfoto)
    filename = x1foto + ".png"
    carpeta2 = str(carpeta1)
    p = os.path.sep.join((carpeta2, filename))
    print (p)
    sinmil=int (int(cronometro(crono)) / 10000)
    cv2.putText(frame, format(str(sinmil)),(10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    print (filename)
    cv2.imwrite(p, frame.copy())
    return 
def segundos(hhmmss):
    horas = hhmmss.hour
    minutos = hhmmss.minute
    segundos = hhmmss.second
    hhmmss_seg = (horas * 60 * 60) + (minutos * 60) + segundos 
    return hhmmss_seg
# Archivo de configuracion
import ConfigParser
#import imutils
from gpiozero import Button
#button = Button(21)
config = ConfigParser.ConfigParser()
config.read("/media/usb0/config/modos1.conf")
#Declaracion de variables    
firstFrame = None
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
#variables de tiempo
ahora = datetime.datetime.now()
crono = datetime.datetime.now()
compara = "Detected"
contar = 1
xfoto = 0
firstFn = reloj(r)
foto = reloj(f)
carpeta = nom("/media/usb0/" + no1)
print (carpeta)
carpeta1 = carpeta
print (carpeta1)
os.mkdir(carpeta)
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (int(vgh),int(vgw))
        camera.framerate = int(frt)
        camera.exposure_mode = em
        camera.shutter_speed= int(ss)
        camera.video_stabilization = True
        time.sleep(0.50)
        k = 0
        while True:
            stream.truncate(0)
            camera.capture(stream, format="rgb", use_video_port=True)
            text = "NOT Detected"
            gray = cv2.cvtColor(stream.array,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            ahora = datetime.datetime.now()
            if  nube == "si":
                if k < 5:
                    k=k+1
                    if firstFrame is None:
                        firstFrame = gray
                        continue
                else:
                    firstFrame = None
                    firstFrame = gray
                    k=0
                    continue
            else:
                if  segundos(ahora) < segundos(firstFn):
                    if firstFrame is None:
                        firstFrame = gray
                        continue
                else:
                    firstFrame = None
                    firstFrame = gray
                    firstFn = reloj(int(r))
                    continue
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, vc, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            contar1 = 0
            for c in cnts:
                if cv2.contourArea(c) < a:
                    continue
                if contar1 > 20:
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(stream.array, (x - 10, y -10), (x + w+20, y + h+20), (0, 255, 0), 2)
                text = "Detected"
                contar1 = contar1 + 1
            cv2.putText(stream.array, "Status: {}".format(text), (10, 20),
	            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(stream.array, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, stream.array.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.putText(stream.array, format(str(xfoto)),(10, stream.array.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            ahora = datetime.datetime.now()
            if text == compara:
                print ("hola foto")
                if f == 0:
                    xfoto= xfoto+1                
                    fotocap(xfoto, carpeta1, stream.array, str(no1))
                    print(xfoto)
                elif segundos(ahora) >= segundos(foto):
                    fotocap(xfoto, carpeta1, stream.array, str(no1))
                    foto=reloj(int(f))
                    xfoto= xfoto+1
                    print(xfoto)
            #frame = imutils.resize(stream.array, width=400)
            #cv2.imshow('frame', frame) 
            #if button.is_pressed:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stream.seek(0)
            stream.truncate()
        stream.close()
        cv2.destroyAllWindows()
    
