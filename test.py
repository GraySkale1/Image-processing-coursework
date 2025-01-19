import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()

Img = ImageTk.PhotoImage(Image.open('fruits.png'))

real = ImageTk.getimage