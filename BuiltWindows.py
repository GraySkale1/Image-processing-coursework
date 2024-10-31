import os
import tkinter as tk
from PIL import Image
from tkinter.filedialog import askopenfilename
import tkinter as tk

EXTS = Image.registered_extensions()

ButtonTemplate = {
    "text" : "Click Me", 
    "activebackground" : "blue", 
    "activeforeground" : "white",
    "anchor" : "center",
    "bd" : 3,
    "bg" : "lightgray",
    "cursor" : "hand2",
    "disabledforeground" : "gray",
    "fg" : "black",
    "font" : ("Arial", 12),
    "height" : 2,
    "highlightbackground" : "black",
    "highlightcolor" : "green",
    "highlightthickness" : 2,
    "justify" : "center",
    "overrelief" : "raised",
    "padx" : 10,
    "pady" : 5,
    "width" : 15,
    "wraplength" : 100}

button_params = {
    "text": "Load Image",
    "bg": "#4CAF50",                  
    "fg": "white",                    
    "font": ("Helvetica", 12, "bold"), 
    "width": 15,                      
    "height": 2,                      
    "borderwidth": 2,                 
    "relief": "raised",               
    "padx": 10,                       
    "pady": 10                        
}

def ButtonBuilder(window:tk.Tk, TemplateDict:dict = button_params, DictOverride:dict = {}, function = None):
    """Returns a tkinter button with the specifications of the input template. DictOverride can be used to make any changes to the template's values"""
    
    #Prevents double declaration of button attributes
    if DictOverride != {}:
        for entry in DictOverride.keys():
            if entry in TemplateDict.keys():
                del TemplateDict[entry]

    return tk.Button(master=window, command=function, **TemplateDict, **DictOverride)


    

class GenericWindow():
    def __init__(self, width:int, height:int, title:str):
        self.display = tk.Tk()
        self.width, self.height = width, height
        self.display.minsize(width, height)
        self.display.resizable(False, False)
        self.display.config(width=width, height=height)
        self.display.title = title

    def run(self):
        self.display.mainloop()

    def quit(self):
        self.display.destroy()


class LoadPage(GenericWindow):
    def __init__(self, width:int, height:int, title:str):
        super().__init__(width, height, title)

        self.path = ''
        button = ButtonBuilder(self.display, DictOverride={"text":"Load image"}, function=self.UserFileRequest)
        button.pack(padx=20, pady=round(self.height * 0.5))

    #def run(self):
        """Runs until self.path has a value"""

    def UserFileRequest(self):
        """Prompts user to open file and returns path. 'ext' used to specify legal file extensions"""
        tk.Tk().withdraw()
        self.path = askopenfilename()
        if self.path != '':
            #Closes window if file has correct extension
            filename, FileExtension = os.path.splitext(self.path)
            if FileExtension in EXTS:
                self.quit()

class FormPage(GenericWindow):
    def __init__(self, width:int, height:int, title:str):
        super().__init__(width, height, title)
        first_name_label = tk.Label(self.display, text="First Name:")
        first_name_label.pack()
        first_name_entry = tk.Entry(self.display)
        first_name_entry.pack()

    
