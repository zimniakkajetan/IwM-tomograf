#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog

from threading import *
from _thread import *

import numpy as np
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage import data, io

from PIL import ImageTk, Image
import PIL
class obraz():
    wejsciowy = []
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Tomograf")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        self.grid(padx=4,pady=4)

        # creating image canvases
        self.inputCanvas = Canvas(self,width=200, height=200,bg='white')
        self.inputCanvas.create_rectangle(2,2,200,200)
        self.inputCanvas.create_text(100,100,text="Obraz wejściowy")
        self.inputCanvas.grid(row=0,column=0)

        self.sinogramCanvas = Canvas(self, width=80,height=200,bg='white')
        self.sinogramCanvas.create_rectangle(2,2,80,200)
        self.sinogramCanvas.create_text(50,50,text="Sinogram")
        self.sinogramCanvas.grid(row=0,column=1)

        self.outputCanvas = Canvas(self,width=200,height=200,bg='white')
        self.outputCanvas.create_rectangle(2,2,200,200)
        self.outputCanvas.create_text(100,100,text="Obraz wyjściowy")
        self.outputCanvas.grid(row=0,column=2)

        self.uploadInputButton = Button(self,text="Wgraj obraz",command=self.upload_input_file)
        self.uploadInputButton.grid(row=1,column=0,pady=2)

        xpadding=10
        top_padding=20
        bottom_padding=5
        Label(self,text="Parametry:").grid(row=2,column=0,pady=(top_padding,bottom_padding))

        Label(self,text="Liczba detektorów:").grid(row=3,column=0,sticky='w',padx=xpadding)
        self.detectorsEntry=Entry(self,width=4,justify=RIGHT)
        self.detectorsEntry.grid(row=3,column=0,sticky='e',padx=xpadding)

        Label(self,text="Kąt przesunięcia:").grid(row=4,column=0,sticky='w',padx=xpadding)
        self.angleEntry = Entry(self,width=4,justify=RIGHT)
        self.angleEntry.grid(row=4,column=0,sticky='e',padx=xpadding)

        Label(self,text="Rozwartość:").grid(row=5,column=0,sticky='w',padx=xpadding)
        self.coneWidthEntry=Entry(self,width=4,justify=RIGHT)
        self.coneWidthEntry.grid(row=5,column=0,sticky='e',padx=xpadding)

        Label(self,text="Liczba iteracji[%]:").grid(row=2,column=1,columnspan=2,pady=(top_padding,bottom_padding))

        self.speedSlider = Scale(self,from_=0,to=100,orient=HORIZONTAL,length=250)
        self.speedSlider.grid(row=3,column=1,columnspan=2,rowspan=2)

        self.startButton = Button(self,text="Start",command=self.makeSinogram1, width=8)
        self.startButton.grid(row=6,column=2,sticky='e',padx=20,pady=10)

        self.set_default_values()
        self.master.update()

    def set_default_values(self):
        self.speedSlider.set(50)
        self.detectorsEntry.insert(END,50)
        self.angleEntry.insert(END,1)
        self.coneWidthEntry.insert(END,90)

    def upload_input_file(self):
        filename = filedialog.askopenfilename(filetypes=[('Image','jpg jpeg png gif')])
        if filename != "": self.set_input_image(filename)

    def set_image(self,path,canvas):
        img = Image.open(path)
        print(img)
        temp = np.array(img.convert('L'))

        img = img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)

        obraz.wejsciowy = temp

        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor=NW)

    def set_input_image(self,path):
        self.set_image(path,self.inputCanvas)

    def set_sinogram_image(self,path):
        self.set_image(path,self.sinogramCanvas)

    def set_output_image(self,path):
        self.set_image(path,self.outputCanvas)

    def bresenhamLine(self, x1, y1, x2, y2):
        line = []
        if (x1 <= x2):
            xi = 1
        else:
            xi = -1
        if (y1 <= y2):
            yi = 1
        else:
            yi = -1

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        x = x1
        y = y1
        line.append([int(x), int(y)])
        if (dx >= dy):
            ai = (dy - dx) * 2
            bi = dy * 2
            d = bi - dx
            while (x != x2):
                if (d >= 0):
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    x += xi
                line.append([int(x), int(y)])
        else:
            ai = (dx - dy) * 2
            bi = dx * 2
            d = bi - dy
            while (y != y2):
                if (d >= 0):
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    y += yi
                line.append([int(x), int(y)])

        return line

    def makeSinogram1(self):
        start_new_thread(self.makeSinogram, ())

    '''  class myThread(Thread):
        def __init__(self):
            Thread.__init__(self)

        def run(self):
            print("Starting ")
            Window.makeSinogram()
            print ("Exiting ")'''

    def makeSinogram(self):
        pic = obraz.wejsciowy

        #numberOfDetectors = 50
        numberOfDetectors = int(self.detectorsEntry.get())
        #alpha = 1
        alpha = float(self.angleEntry.get())
        #rozpietosc = 90
        rozpietosc = float(self.coneWidthEntry.get())
        time = 0
        if(self.speedSlider.get() != 0): #LICZENIE LICZBY ITERACJI
            time = 180 / ((180/alpha) * (int(self.speedSlider.get())/100))
        rozpietoscRadiany = rozpietosc * np.pi / 180;
        pic_size = len(pic[0])

        r = pic_size

        sinogram = []
        lines = []

        i = 0
        while i < 180:
            sinogram.append([])
            lines.append([])
            katRadiany = i * np.pi / 180
            x0 = r * np.cos(katRadiany)
            y0 = r * np.sin(katRadiany)
            x0 = int(x0) + np.floor(pic_size / 2)
            y0 = int(y0) + np.floor(pic_size / 2)

            for detector in range(0, numberOfDetectors):
                x1 = r * np.cos(katRadiany + np.pi - rozpietoscRadiany / 2 + detector * (
                rozpietoscRadiany / (numberOfDetectors - 1)))
                y1 = r * np.sin(katRadiany + np.pi - rozpietoscRadiany / 2 + detector * (
                rozpietoscRadiany / (numberOfDetectors - 1)))

                x1 = int(x1) + np.floor(pic_size / 2)
                y1 = int(y1) + np.floor(pic_size / 2)

                line = self.bresenhamLine(x0, y0, x1, y1)
                pixel = np.float(0)
                pixLicz = int(0)
                for [x, y] in line:
                    if x >= 0 and y >= 0 and x < pic_size and y < pic_size:
                        pixel += float(pic[x, y])
                        pixLicz += 1

                if pixLicz > 0:
                    sinogram[-1].append(pixel / pixLicz)
                else:
                    sinogram[-1].append(0)
                lines[-1].append([x0, y0, x1, y1])
            i += alpha

            if (time!= 0 & (int(i)+1) % (int(time)+1) == 0):
                self.setSinogramOutput(sinogram)

        self.setSinogramOutput(sinogram)
        #obraz.sinogram = np.array(sinogram)
        start_new_thread(self.makePicture, (sinogram,lines,pic))

        return sinogram, lines

    def setSinogramOutput(self,sin):
        #self.sinogramCanvas.delete("all")
        self.sinogramCanvas.image = ImageTk.PhotoImage(PIL.Image.fromarray(np.array(sin)))
        self.sinogramCanvas.create_image(0, 0, image=self.sinogramCanvas.image, anchor=NW)

    def setPicture2Output(self,pic):
        #self.outputCanvas.delete("all")
        self.outputCanvas.image = ImageTk.PhotoImage(PIL.Image.fromarray((pic)))
        self.outputCanvas.create_image(0, 0, image=self.outputCanvas.image, anchor=NW)

    def makePicture(self, sinog, lines, pic):
        print("start make picture")
        picture2 = np.zeros([np.shape(pic)[0], np.shape(pic)[1]])
        a = np.shape(sinog)[0]
        b = np.shape(sinog)[1]
        time = 0
        if (self.speedSlider.get() != 0):  # LICZENIE LICZBY ITERACJI
            time = 180 / (a * (int(self.speedSlider.get()))/100)
        for i in range(0, a, 1):
            for j in range(0, b, 1):
                x0, y0, x1, y1 = lines[i][j]
                line = self.bresenhamLine(x0, y0, x1, y1)
                for [x, y] in line:
                    if x >= 0 and y >= 0 and x < np.shape(pic)[0] and y < np.shape(pic)[1]:
                        picture2[x][y] += sinog[i][j]
            if (time!= 0 & (int(i)+1) % (int(time)+1) == 0):
                self.setPicture2Output(picture2)
        self.setPicture2Output(picture2)
        #print(picture2)
        return picture2

root = Tk()
root.geometry("620x400")

app=Window(root)



root.mainloop()
