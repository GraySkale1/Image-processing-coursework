import tkinter as tk

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

def ButtonBuilder(window:tk.Tk, TemplateDict:dict = ButtonTemplate, DictOverride:dict = {}, function = None):
    """Returns a tkinter button with the specifications of the input template. DictOverride can be used to make any changes to the template's values"""
    
    #Prevents double declaration of button attributes
    if DictOverride != {}:
        for entry in DictOverride.keys():
            if entry in TemplateDict.keys():
                del TemplateDict[entry]

    return tk.Button(master=window, command=function, **TemplateDict, **DictOverride)


    
