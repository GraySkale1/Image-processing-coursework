import tkinter as tk


class GenericWindow():
    def __init__(self, width:int, height:int, title:str):
        self.display = tk.Tk()
        self.display.config(width=width, height=height)
        self.display.title = title

    def run(self):
        self.display.mainloop()

new = GenericWindow(500, 500, "Generic")
new.run()