

from tkinter import *
from PIL import *
from PIL import ImageTk,Image
from tkinter import ttk,messagebox
from ttkthemes import ThemedTk as team
import sys
from check_music import Check_music
import os,time,datetime


class HomePage:
    def __init__(self,root):
        self.root = root
        self.root.title("Homepage")
        self.root.geometry("850x500+300+50")
        self.root.configure(background="black")
        self.root.resizable(False,False)
        
        #background image

        self.bg =PhotoImage(file="image/2.png")
        self.bg_image = ttk.Label(self.root,image=self.bg).place(x=0,y=0)

        self.start =PhotoImage(file="image/start.png")
        start_label = Label(self.root,text="Genre of Music",font=("Goudy old style",25,"bold")).place(x=230,y=450,width=320,height=50)

        start_btn = Button(self.root,image=self.start,command=self.login_function,bg="black",bd=0).place(x=730,y=450,width=120,height=50) 


    def login_function(self):
        return Check_music(self.root)
        pass
        

if __name__ == "__main__":
   root = team(theme="black")
   obj = HomePage(root)
   root.mainloop()


