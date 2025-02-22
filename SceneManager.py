import os
import re
import numpy as np
import tkinter as tk
from PIL import Image, ImageOps, ImageTk, ImageChops, ImageFilter
import PIL
from tkinter.filedialog import askopenfilename
from functools import partial
from datetime import datetime


class SceneManager():
    def __init__(self, DefaultShape:tuple):
        self.CurSceneID = 0
        self.ImageDir = ''

        self.width, self.height = DefaultShape
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.RefreshPage()
        self.root.mainloop()

    def _LoadScene(self, SceneClass):
        SceneClass.Build(self)

    def WipePage(self):
        for child in self.root.winfo_children():
            child.destroy()


    def _PickScene(self):
        """Returns the scene class that corrolates to the current scene ID (CurSceneID)"""
        match self.CurSceneID:
            case 0:
                return SceneManager.Start()
            case 1:
                return SceneManager.ImageEditor()
            case _:
                raise NotImplementedError(f'Scene {self.CurSceneID} has no class definition')

    def RefreshPage(self):
        """Clears all widgets, determines the current scene and displays its widgets"""
        self.WipePage()

        SceneClass = self._PickScene()
        self._LoadScene(SceneClass)


    #~~~~~~~~~~~~~~~~~~~~~~~
    # Inner classes

    class Start():
        def Build(self, manager:"SceneManager"):
            global PhotoName
            global DateOfCapture
            global DateOfSub
            global Description
            global Photographer

            PhotoName = tk.StringVar(manager.root)
            DateOfCapture = tk.StringVar(manager.root)
            DateOfSub = tk.StringVar(manager.root)
            Description = tk.StringVar(manager.root)
            Photographer = tk.StringVar(manager.root)

            VarNames = [PhotoName, Photographer, DateOfCapture, DateOfSub, Description]
            FormText = ["Photo Name:", "Photographer", "Date of Capture: (dd/mm/yyyy)", "Date of Submission: (dd/mm/yyyy)", "Description: (250 character limit)"]
            FormList = []

            for i, text in enumerate(FormText):
                form = self.CreateForm(text, manager.root, VarNames[i])

            self.ValidImage = False 

            button = tk.Button(manager.root, text="Enter", command=partial(self.ButtonPress, manager), padx=25, pady=15)
            button.pack()


        def ButtonPress(self, manager:"SceneManager"):
            """Validates all inputs from forms then switches scenes"""

            manager.ImageDir = self.GetUserImage(manager)

            valid = self.ValidateForm()

            
            if valid == True:
                self.SwitchScenes(manager)

        def ValidateForm(self)-> bool:
            """Checks the data in the form page for invalid data and returns False unless all forms are correct"""
            ErrorMessage = ''

            DesText = Description.get()
            PhotoText = PhotoName.get()
            DateCapText = DateOfCapture.get()
            DateSubText = DateOfSub.get()
            PhotoMaker = Photographer.get()

            #Checks photo name
            if PhotoText == '':
                ErrorMessage += "- File name can't be empty\n"
            else:
                try:
                    F = open(f'{PhotoText}.tmp', 'x')
                    os.remove(f'{PhotoText}.tmp')
                except:
                    ErrorMessage += '- File name invalid.\n'

            #checks photographer
            if PhotoMaker == "":
                ErrorMessage += "- Photographer can't be empty\n"

            #Checks capture date
            pmatch = re.search(string=DateCapText, pattern="[0-9]{2}/[0-9]{2}/[0-9]{4}")
            if pmatch == None:
                ErrorMessage += "- Invalid capture date\n"
            
            #Checks submission date
            pmatch = re.search(string=DateCapText, pattern="[0-9]{2}/[0-9]{2}/[0-9]{4}")
            if pmatch == None:
                ErrorMessage += "- Invalid submission date\n"

            #Checks description
            if len(DesText) >= 250:
                ErrorMessage += '- Description must be less than 250 characters.\n'

            if ErrorMessage != '':
                ErrorMessage = ErrorMessage[0:-1]
                self.RaiseError(title="FormError", text=ErrorMessage)
                return False
            
            return True


            
        def GetUserImage(self, manager:"SceneManager"):
            "Asks the user to select an image and validates it"
            ImDir = askopenfilename()
            self.ValidImage = False
            #validates if image is in a usable format
            try:
                img = Image.open(ImDir)
                img.verify()
                self.ValidImage = True
            except:
                self.RaiseError(title="FileError", text="Unsupported File Type")
                ImDir = ""
            return ImDir


        def SwitchScenes(self, manager:"SceneManager"):
            """Method that tells the SceneManager container to change scenes"""

            manager.CurSceneID = 1
            manager.RefreshPage()


        def RaiseError(self, title, text):
            ErrorMsg = tk.messagebox.showerror(title=title, message=text)
            #ErrorMsg.showerror()

        @staticmethod
        def CreateForm(text:str, root:tk.Tk, TextVar:str):
            """Creates and packs a label and corresponding entry widget"""
            label = tk.Label(root, text=text, padx=25, pady=1)
            label.pack()
            entry = tk.Entry(root, textvariable=TextVar)
            entry.pack()





    class ImageEditor():
        def Build(self, manager:"SceneManager"):
            """This method is called when the scene needs to be rendered by the SceneManager\n It creates and renders all the elements to the screen"""
            self.blur = 0
            self.manager = manager

            #setting up image to be rendered 
            self.ImageContainer = tk.Label(manager.root)
            self.Img = ImageTk.PhotoImage(Image.open(manager.ImageDir))
            self.DisplayImg = self.Img

            manager.root.geometry(f"{self.Img.width() + 200}x{self.Img.height()+200}")
            manager.root.rowconfigure(5, {'minsize': 30})
            manager.root.columnconfigure(4, {'minsize': 30})

            self.ImageContainer.grid(row=0,column=4,rowspan=4, columnspan=1, sticky='e')
            self.ImageContainer.configure(image=self.DisplayImg)
            
            #setting up buttons to process the image
            self.GrayScaleButton = tk.Button(manager.root, text="Grayscale", command=self.GrayScale, padx=25, pady=25)
            self.GrayScaleButton.grid(row=0,column=2)
            self.UndoButton = tk.Button(manager.root, text="Undo", command=self.Undo, padx=25, pady=25)
            self.UndoButton.grid(row=3, column=2)
            self.InvertButton = tk.Button(manager.root, text="Invert image", command=self.Invert, padx=25, pady=25)
            self.InvertButton.grid(row=1,column=2)
            self.BlurButton = tk.Button(manager.root, text="Blur image", command=self.BlurImage, padx=25, pady=25)
            self.BlurButton.grid(row=2,column=2)
            self.BlurButton = tk.Button(manager.root, text="Save", command=self.SaveImage, padx=25, pady=25)
            self.BlurButton.grid(row=4,column=2)

        def SaveImage(self):
            FinalImage = ImageTk.getimage(self.DisplayImg)
            FinalImage.save(fp=f'{PhotoName.get()}.png', format='png')
            self.manager.CurSceneID = 0
            self.manager.root.geometry(f"{self.manager.width}x{self.manager.height}")
            self.manager.RefreshPage()
            

        def UpdateImage(self):
            """Swaps the data from self.DisplayImg and self.Img and rerenders self.DisplayImage\n (all processes are performed on self.Img, not on self.DisplayImg)"""
            temp = self.DisplayImg
            self.DisplayImg = self.Img
            self.Img = temp

            self.ImageContainer.configure(image=self.DisplayImg)

        def Undo(self):
            """Undoes the last performed action (only remembers last action)"""
            self.UpdateImage()


        def ContinuityFix(self):
            """Should be run before any process is performed on the image to prevent disconnect between self.Img and self.DisplayImg"""
            if self.DisplayImg != self.Img:
                self.Img = self.DisplayImg


        def GrayScale(self):
            self.ContinuityFix()

            RawImage = ImageTk.getimage(self.Img)
            GrayImage = ImageOps.grayscale(RawImage)
            self.Img = ImageTk.PhotoImage(GrayImage)

            self.UpdateImage()

        def Invert(self):
            self.ContinuityFix()

            RawImage = ImageTk.getimage(self.Img)
            pixels = np.array(RawImage)

            if pixels.ndim == 3 and pixels.shape[2] == 4:  
                
                rgb = pixels[:, :, :3]  
                alpha = pixels[:, :, 3]  
                InvertedRBG = 255 - rgb  
                InvertedPixels = np.dstack((InvertedRBG, alpha))  
            else:
                InvertedPixels = 255 - pixels

            InvertedImage = Image.fromarray(InvertedPixels.astype('uint8'), 'RGBA')
            self.Img = ImageTk.PhotoImage(InvertedImage)

            self.UpdateImage()

        def BlurImage(self):
            self.ContinuityFix()

            self.blur += 1

            RawImage = ImageTk.getimage(self.Img)
            blur = RawImage.filter(ImageFilter.GaussianBlur(self.blur))
            self.Img = ImageTk.PhotoImage(blur)

            self.UpdateImage()

if __name__ == '__main__':
    import main