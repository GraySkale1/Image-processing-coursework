import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from functools import partial
from datetime import datetime


class SceneManager():
    def __init__(self, shape:tuple):
        self.CurSceneID = 0
        self.ImageDir = ''

        width, height = shape
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
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

            PhotoName = tk.StringVar(manager.root)
            DateOfCapture = tk.StringVar(manager.root)
            DateOfSub = tk.StringVar(manager.root)
            Description = tk.StringVar(manager.root)

            VarNames = [PhotoName, DateOfCapture, DateOfSub, Description]
            FormText = ["Photo Name:", "Date of Capture", "Date of Submission", "Description: (250 character limit)"]
            FormList = []

            for i, text in enumerate(FormText):
                form = self.CreateForm(text, manager.root, VarNames[i])

            

            button = tk.Button(manager.root, text="Enter", command=partial(self.ButtonPress, manager), padx=25, pady=15)
            button.pack()


        def ButtonPress(self, manager:"SceneManager"):
            """Validates all inputs from forms then switches scenes"""

            manager.ImageDir = self.GetUserImage(manager)

            sequence = "%d-%m-%Y"
            DOC = DateOfCapture.get()

            #checks if date is in a valid dd/mm/yyyy
            match = True
            try:
                match = bool(datetime.strptime(DOC, sequence))
            except ValueError:
                match = False

            if match == False:
                self.SwitchScenes(manager)

            
        def GetUserImage(self, manager:"SceneManager"):
            "Asks the user to select an image and validates it"
            ImDir = askopenfilename()
            #validates if image is in a usable format
            try:
                img = Image.open(ImDir)
                img.verify()
            except:
                label = tk.Label(manager.root, text="Invalid format, image type may not be supported or image is corrupted", fg="red", padx=1,pady=1)
                label.pack()
                ImDir = ""
            return ImDir


        def SwitchScenes(self, manager:"SceneManager"):
            """Method that tells the SceneManager container to change scenes"""

            manager.CurSceneID = 1
            manager._PickScene()

        @staticmethod
        def CreateForm(text:str, root:tk.Tk, TextVar:str):
            """Creates and packs a label and corresponding entry widget"""
            label = tk.Label(root, text=text, padx=25, pady=1)
            label.pack()
            entry = tk.Entry(root, textvariable=TextVar)
            entry.pack()


    class ImageEditor():
        def Build(self, manager:"SceneManager"):
            self.ImageContainer = tk.Label(manager.root)
            self.ImageContainer.pack()

            self.Img = ImageTk.PhotoImage(Image.open(Imagemanager.ImageDir))
            self.ImageContainer.configure(image=self.Img)
            self.label.image = self.Img

if __name__ == '__main__':
    import main