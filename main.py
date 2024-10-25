import tkinter as tk
from tkinter.filedialog import askopenfilename
from buttons import *

WIDTH, HEIGHT = 1920, 1080

class GenericWindow():
    def __init__(self, width:int, height:int, title:str):
        self.display = tk.Tk()
        self.width, self.height = width, height
        self.display.minsize(width, height)
        self.display.resizable(False, False)
        self.display.config(width=width, height=height)
        self.display.title = title

    def custom():
        pass


    def run(self):
        self.display.mainloop()

class LoadPage(GenericWindow):
    def __init__(self, width:int, height:int, title:str):
        super().__init__(width, height, title)

        button = ButtonBuilder(self.display, DictOverride={"text":"Load image"}, function=self.UserFileRequest)
        button.pack(padx=20, pady=round(HEIGHT * 0))


    def UserFileRequest(ext:tuple[str] = None):
        """Prompts user to open file and returns path. 'ext' used to specify legal file extensions"""
        tk.Tk().withdraw()
        path = askopenfilename()
        return path





new = LoadPage(round(WIDTH * 0.15), round(HEIGHT * 0.5), "Generic")
new.run()