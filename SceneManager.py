import tkinter as tk
from functools import partial
from datetime import datetime


class SceneManager():
    def __init__(self, shape:tuple):
        self.CurSceneID = 0
        #self.ButtonDicts = [] #list of dicts that can be fed into the ButtonBuilder function

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

            button = tk.Button(manager.root, text="Enter", command=partial(self.SwitchScenes, manager), padx=25, pady=15)
            button.pack()


        def ButtonPress(self, manager:"SceneManager"):
            """Validates all inputs from forms then switches scenes"""
            sequence = "%d-%m-%Y"
            DOC = DateOfCapture.get()

            #checks if date is in a valid dd/mm/yyyy
            match = True
            try:
                match = bool(datetime.strptime(test_str, sequence))
            except ValueError:
                match = Falseformat = "%d-%m-%Y"

            if match == False:
                pass



            self.SwitchScenes(manager)
            

        def SwitchScenes(self, manager:"SceneManager"):
            """Ok look, button presses need to be static methods and pass the outer scene manager as an input (button builder does that)"""

            manager.CurSceneID = 1
            manager._PickScene()

        @staticmethod
        def CreateForm(text:str, root:tk.Tk, TextVar:str):
            """Creates and packs a label and corresponding entry widget"""
            label = tk.Label(root, text=text, padx=25, pady=1)
            label.pack()
            entry = tk.Entry(root, textvariable=TextVar)
            entry.pack()


if __name__ == '__main__':
    import main