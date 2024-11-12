import tkinter as tk
from functools import partial


class Gscene():
    """Generic class that has default functions to prevent N"""
    def ReadButtons(self):
        """Outputs a list of dictionaries that contains the data for the scene's buttons"""
        return []


class SceneManager():
    def __init__(self, shape:tuple):
        self.CurSceneID = 0
        #self.ButtonDicts = [] #list of dicts that can be fed into the ButtonBuilder function

        width, height = shape
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.RefreshPage()
        self.root.mainloop()


    def ButtonBuilder(self, DictTemplate:dict, DictOverride:dict = {}) -> tk.Button:

        # Deletes any elements in DictTemplate that also appear in DictOverride
        for attribute in DictTemplate:
            if attribute in DictOverride:
                del DictTemplate[attribute]

        if "command" in DictTemplate.keys():
            DictTemplate["command"] = partial(DictTemplate["command"], self) #partial creates a peusdo-lambda function that preloads the scenemanager class inside itself

        return tk.Button(self.root, **DictTemplate, **DictOverride)

    def _LoadScene(self, SceneClass:Gscene):
        buttons = SceneClass.ReadButtons()
        for ButtonDict in buttons:
            b = self.ButtonBuilder(DictTemplate=ButtonDict)
            b.pack()

    def WipePage(self):
        raise NotImplementedError


    def _PickScene(self):
        """Returns the scene class that corrolates to the current scene ID (CurSceneID)"""
        match self.CurSceneID:
            case 0:
                return SceneManager.Start()
            case _:
                raise NotImplementedError(f'Scene {self.CurSceneID} has no class definition')

    def RefreshPage(self):
        """Clears all widgets, determines the current scene and displays its widgets"""
        #self.WipePage()

        SceneClass = self._PickScene()
        self._LoadScene(SceneClass)


    #~~~~~~~~~~~~~~~~~~~~~~~
    # Inner classes

    class Start(Gscene):
        def ReadButtons(self):
            return [{"text":"Click Me", "command":self.ButtonClicked, "padx":25, "pady":25}]

        @staticmethod
        def ButtonClicked(manager:"SceneManager"):
            """Ok look, button presses need to be static methods and pass the outer scene manager as an input (button builder does that)"""
            manager.CurSceneID = 1
            manager._PickScene()

if __name__ == '__main__':
    import main