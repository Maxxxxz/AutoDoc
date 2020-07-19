from tkinter import *
from tkinter import filedialog, Tk, Toplevel, messagebox
import pprint
import tkinter as tk
from tkinter.ttk import Combobox
import Pages
from cli import runCLI
import json
import sys
import os

WIDTH = 500
HEIGHT = 500

# Maybe add a 'strip comments' feature

# Load these from JSON in the future with these as defaults?
COMMFILE = "languageComments.json"
REGEXFILE = "languageRegexes.json"
TITLE = "Auto Doc"
VERSION = "0.20.7.18"

#   Application class
class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, relief=tk.GROOVE)
        master.title(TITLE)
        master.geometry("{}x{}".format(WIDTH, HEIGHT))
        master.resizable(width=False, height=False)

        self.pages = [] #init pages list

        self.contentFrame = None

        self.addContent()

        self.pages[0].show()

        self.SELECTED = None
        self.selectedFiles = None

    def addContent(self, contentFrame=None):
        self.pages.append(Pages.Menu(WIDTH, HEIGHT))
        self.pages.append(Pages.DocumenterPage(WIDTH, HEIGHT))

        self.contentFrame = tk.Frame(self.master, width=100, height=100)
        self.contentFrame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        for page in self.pages:
            page.place(in_=self.contentFrame, x=0, y=0, relwidth=1, relheight=1)
            page.setApp(self)

        # # binds
        # # unbind if previously bound
        # self.unbind_all("<Control-Key-0>")
        # self.unbind_all("<Control-Key-1>")
        # # now bind the controls
        # self.bind_all("<Control-Key-0>", self.pages[0].show)  # main menu
        # self.bind_all("<Control-Key-1>", self.pages[1].show)  # Page 2

    def setContent(self, lang, files):
        self.SELECTED = lang
        self.selectedFiles = files
        print(self.SELECTED)
        print(self.selectedFiles)
        self.pages[1].setLang(lang)
        self.pages[1].setFiles(files)

    def beginDocumenting(self):
        if self.SELECTED is None or self.selectedFiles is None:
            messagebox.showinfo("Error", "Please Select a Language and Files")
        else:
            if self.checkLangInJSON():
                self.pages[1].postInit()  # init documentor object here
                self.pages[1].show()

    def checkLangInJSON(self):
        with open('./json/languageComments.json', encoding='utf-8') as comInfo:
            data1 = json.loads(comInfo.read())

        if self.SELECTED in data1:
            self.pages[1].setLangCom(data1[self.SELECTED])
        else:
            messagebox.showerror("Language not found", "Language: {} not found in {}".format(self.SELECTED, COMMFILE))
            return False
        
        with open('./json/languageRegexes.json', encoding='utf-8') as regInfo:
            data2 = json.loads(regInfo.read())

        if self.SELECTED in data2:
            rx = data2[self.SELECTED]
            if rx != "":
                self.pages[1].setLangRx(rx)
            else:
                messagebox.showerror("Illegal Regex", "Language: {} regex cannot be blank".format(self.SELECTED))
                return False
        else:
            messagebox.showerror("Language not found", "Language: {} not found in {}".format(self.SELECTED, REGEXFILE))
            return False

        return True

    def restart(self, files=None):
        self.SELECTED = None
        self.selectedFiles = files
        self.pages[0].restart()
        self.pages[0].show()

def handleArgs():
    if sys.argv[1] == "-help":
        print("{} Commands:".format(TITLE))
        print("-help: Shows this message.")
        print("-gui: Launches the gui version of {}.".format(TITLE))
        print("-version: Shows the current version of {}.".format(TITLE))
        # print("-update: Attempts to update {}.".format(TITLE)) 
    elif sys.argv[1] == "-gui":
        root = tk.Tk()
        app = Application(root)
        app.pack()
        root.mainloop()
    elif sys.argv[1] == "-version":
        print("{}".format(VERSION))
    else:
        print("Unknown argument {}.".format(sys.argv[1]))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        handleArgs()
    elif len(sys.argv) == 1:
        cl = cli.CLI()
        cl.runCLI()
    else:
        print("Too many arguments. Try running with -help.")
else:
    pass