#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image

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

        self.sinogramCanvas = Canvas(self, width=200,height=200,bg='white')
        self.sinogramCanvas.create_rectangle(2,2,200,200)
        self.sinogramCanvas.create_text(100,100,text="Sinogram")
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

        Label(self,text="Prędkość przetwarzania:").grid(row=2,column=1,columnspan=2,pady=(top_padding,bottom_padding))

        self.speedSlider = Scale(self,from_=0,to=100,orient=HORIZONTAL,length=250)
        self.speedSlider.grid(row=3,column=1,columnspan=2,rowspan=2)

        self.startButton = Button(self,text="Start",width=8)
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
        img = img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor=NW)

    def set_input_image(self,path):
        self.set_image(path,self.inputCanvas)

    def set_sinogram_image(self,path):
        self.set_image(path,self.sinogramCanvas)

    def set_output_image(self,path):
        self.set_image(path,self.outputCanvas)

root = Tk()
root.geometry("620x400")

app=Window(root)



root.mainloop()
