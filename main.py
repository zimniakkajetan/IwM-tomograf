#!/usr/bin/python3
from tkinter import *
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
        self.inputCanvas.grid(row=0,column=0)

        self.sinogramCanvas = Canvas(self, width=200,height=200,bg='white')
        self.sinogramCanvas.grid(row=0,column=1)

        self.outputCanvas = Canvas(self,width=200,height=200,bg='white')
        self.outputCanvas.grid(row=0,column=2)

        self.uploadInputButton = Button(self,text="Wgraj obraz")
        self.uploadInputButton.grid(row=1,column=0)

        self.paramsLabel = Label(self,text="Parametry:").grid(row=2,column=0)
        self.master.update()

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

app.set_input_image('foto1/Kwadraty2.jpg')
app.set_sinogram_image('foto1/Kolo.jpg')
app.set_output_image('foto1/Kropka.jpg')

root.mainloop()
