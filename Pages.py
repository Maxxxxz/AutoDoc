import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import Documenter as dc
from typing import List

import json

# Add self.approot variable so all child pages have direct access to the app root
class Page(tk.Frame):
    def __init__(self):
        self.LANG = None
        self.FILES = None
        self.NAME = "AutoDoc"
        self.APP = None
        tk.Frame.__init__(self)

    def show(self, event=None):
        self.lift()

    def setLang(self, lang):
        self.LANG = lang

    def setFiles(self, files):
        self.FILES = files

    def setApp(self, app):
        self.APP = app

#   Main menu
class Menu(Page):
    def __init__(self, w, h):
        Page.__init__(self)
        self.selectedFiles = None

        with open('./json/supportedLanguages.json', encoding='utf-8') as langInfo:
            self.langs = json.loads(langInfo.read())

        self.langs = self.langs["Languages"]

        self.w = w
        self.h = h
        ###############################
        #   Language Selection Combobox
        self.cb = ttk.Combobox(self, textvariable=tk.StringVar(),
                       values=self.langs,
                       state="readonly")    # Drop down menu
        self.cb.set("Select Language")
        self.cb.bind("<<ComboboxSelected>>",
                lambda event, argu=self.cb: self.langSelectEvent(event, argu))  # event to grab selected language
        self.cb.place(x=(w/2), y=((h/2) - (h/2.25)), anchor="center")
        ###############################

        ###############################
        #   Selected Files Textbox
        self.textbox = tk.Text(self)
        self.textbox.config(width=50, height=23)
        self.textbox.place(x=(w/2), y=((h/2) + 1.5 * (h/24)), anchor="center")
        self.textbox.config(state=tk.DISABLED)
        ###############################

        # Maybe in the future add a select more option to simply add to the list + an option to remove certain files?
        ###############################
        #   File Select Button
        self.selectButton = tk.Button(self, text="Select Files", width=15, command=lambda: self.openFiles())
        self.selectButton.place(x=(w/2), y=((h/2) - (h/2.75)), anchor="center")
        ###############################

        ###############################
        #   Document Button
        self.docButton = tk.Button(self, text="Document", width=30, command=lambda: self.master.children["!application"].beginDocumenting())
        self.docButton.place(x=(w/2), y=((h/2) + (h/2.15)), anchor="center")
        ###############################

    def restart(self):
        # re-init
        self.cb.set("Select Language")
        self.selectedFiles = None
        self.textbox.config(state=tk.NORMAL)
        self.textbox.delete('1.0', tk.END)
        self.textbox.config(state=tk.DISABLED)
        # self.destroy()

    def openFiles(self):
        self.selectedFiles = filedialog.askopenfilenames(title="Select files")
        self.textbox.config(state=tk.NORMAL)
        self.textbox.delete('1.0', tk.END)  # strange behaviour when not using '1.0'
        self.textbox.insert(tk.END, '\n'.join(self.selectedFiles))
        self.textbox.config(state=tk.DISABLED)
        if self.selectedFiles is not None:
            self.master.children["!application"].setContent(self.LANG, self.selectedFiles)

    def langSelectEvent(self, event, argu):
        self.LANG = argu.get()
        self.master.children["!application"].setContent(self.LANG, self.selectedFiles)

#   Documentor pages
class DocumenterPage(Page):
    def __init__(self, w, h):
        Page.__init__(self)

        ##########################
        #   Initialize Documentor
        # set this later
        self.doc = None
        ##########################

        ##########################
        #   Initialize json data
        self.langcom = None
        self.langregex = None
        ##########################

        ##########################
        #   Initialize variables
        self.curfunccounter = -1
        self.linesDict: dict = {}
        self.keys: List = []
        self.comments: dict = {}
        self.localname = None
        self.w = w
        self.h = h
        ##########################

        ##########################
        #   Show the current File
        self.curFileBox = tk.Text(self)
        self.curFileBox.config(width=50, height=1) # 1 line tall, 50 chars long
        self.curFileBox.place(x=(w/2), y=((h/2) - (h/2.15)), anchor="center")
        self.curFileBox.insert(tk.END, "file.ext")
        self.curFileBox.config(state=tk.DISABLED)  # disable after inserting
        ##########################

        ##########################
        #   Show the current Function
        self.functionbox = tk.Text(self)
        self.functionbox.config(width=50, height=1) # 1 line tall, 50 chars long
        self.functionbox.place(x=(w/2), y=((h/2) - (h/2.35)), anchor="center")
        self.functionbox.insert(tk.END, "def function()")
        self.functionbox.config(state=tk.DISABLED)  # disable after inserting
        ##########################

        ##########################
        #   Comment Editor
        self.commentbox = tk.Text(self)
        self.commentbox.config(width=50, height=25)
        self.commentbox.place(x=(w/2), y=(h/2), anchor="center")
        self.commentbox.insert(tk.END, "function description")
        ##########################

        ##########################
        #   Next Button
        self.nextButton = tk.Button(self, text="Next Function", width=15, command=lambda: self.but_nextFunc())
        self.nextButton.place(x=((w/2) + (w/4)), y=((h/2) + (h/2.25)), anchor="center")
        ##########################

        ##########################
        #   No Doc
        self.noDocButton = tk.Button(self, text="No Documentation", width=15, command=lambda: self.but_noDoc())
        self.noDocButton.place(x=(w / 2), y=((h / 2) + (h / 2.25)), anchor="center")
        ##########################

        ##########################
        #   Previous Button
        self.prevButton = tk.Button(self, text="Previous Function", width=15, command=lambda: self.but_prevFunc())
        self.prevButton.place(x=((w/2) - (w/4)), y=((h / 2) + (h / 2.25)), anchor="center")
        ##########################

        #label = tk.Label(self, text="Page 2")
        #label.place(x=(w/2), y=25, anchor="center")

    def postInit(self): # actually init documentor here
        self.doc = dc.Documenter(self.LANG, self.FILES, self.langregex, self.APP)
        # initial page content put in here

        # add logic to check if lines dict has any content in it

        self.linesDict = self.doc.getLines()

        print(self.linesDict)
        self.updateKeys()
        if self.checkValidLines():
            self.curfunccounter = 0
            self.updateBoxes()
            self.show()
        else:
            self.nextFileLogic()

    def setLangCom(self, com):
        self.langcom = com

    def setLangRx(self, rx):
        self.langregex = rx

    def restart(self):
        # re-init
        self.doc = None
        self.curfunccounter = -1
        self.linesDict: dict = {}
        self.keys: List = []
        self.comments: dict = {}
        self.localname = None

        # del self.doc
        # self.destroy()

    def updateKeys(self):
        self.keys = list(self.linesDict.keys())
        self.keys.sort()

    # need to add keys to the self.comments so I can pass that to comment
    def but_nextFunc(self):
        self.commentLogic()
        if len(self.linesDict) <= len(self.comments) and self.curfunccounter == len(self.linesDict) - 1:    # if no more functions in file to document
            t_choice = messagebox.askyesno("Confirm Documentation of File", "Are you sure you want to add documentation to this file?")
            if t_choice:    # if yes: add documentation
                # print(self.comments)
                self.doc.addComment(self.comments)
                self.nextFileLogic()
            else:   # else just do nothing, lets the user go back and change their info
                pass
        else:       # else just do logic to move onto next function
            # self.commentLogic()
            self.curfunccounter += 1
            # now show the next function
            self.updateBoxes()

            # if len(self.comments) >= (self.curfunccounter + 1):  # if index already exists (index + 1) override current comment at index
            #     self.comments[self.keys[self.curfunccounter]] = self.commentbox.get('1.0', tk.END)
            # else:  # else: append current comment and increment counter
            #     self.comments.append((self.commentbox.get('1.0', tk.END)))

        # print("next func")

    def but_noDoc(self):
        self.commentbox.delete('1.0', tk.END)    # make the comment box empty
        self.but_nextFunc() # just call nextFunc logic, it is the same when the comment box is entirely empty
        # print("no documentation!")

    def but_prevFunc(self):
        self.commentLogic()
        # if len(self.comments) >= (self.curfunccounter + 1):  # if index already exists (index + 1) override current comment at index
        #     self.comments[self.keys[self.curfunccounter]] = self.commentbox.get(1.0, tk.END)
        # else:  # else: append current comment and decrement counter
        #     self.comments.append(self.commentbox.get(1.0, tk.END))

        if self.curfunccounter >= 1:
            self.curfunccounter -= 1
        else:
            messagebox.showinfo("Unable to move to previous function", "You can not move to the previous function, as there is none.")

        # now show the previous function

        self.updateBoxes()

        # print("prev func")

    def nextFileLogic(self):
        self.curfunccounter = 0
        self.doc.nextFile()
        if self.doc.CURFILE == "NO MORE FILES":
            messagebox.showinfo("No More Files", "There are no more files to document in your given list.\nThe program will now return to the menu.")
            self.returnToMenu()
        else:
            self.linesDict = self.doc.getLines()
            self.comments = {}
            if self.checkValidLines():
                self.updateKeys()
            else:
                self.nextFileLogic()
            self.updateBoxes()

    def returnToMenu(self):
        self.APP.restart()
        self.restart()

    def commentLogic(self):

        # print(self.curfunccounter)
        # print(self.keys)
        # print(self.comments)

        # if len(self.comments) >= (self.curfunccounter + 1):  # if index already exists (index + 1) override current comment at index
        toadd = self.commentbox.get(1.0, 'end-1c') # end-1c to not grab the newline at the end
        self.comments[self.keys[self.curfunccounter]] = toadd.split('\n') # split by lines
        # else:  # else: append current comment and increment counter
        #     self.comments.append((self.commentbox.get(1.0, tk.END)))

    def checkValidLines(self) -> bool:
        if len(self.linesDict) < 1:
            messagebox.showerror("No Functions Found",
            "There were no functions found in " + self.doc.CURFILE +
            ".\nThis could be due to a failed regex, or the file simply does not have functions declared in it." +
            "\n" + self.NAME + " will now move on to the next file.")
            return False
        else:
            return True

    def removeNewlines(self):
        # https://stackoverflow.com/a/48223941
        if self.commentbox.get('end-1c', tk.END) == '\n':
            self.commentbox.delete('end-1c', tk.END)

    def getLocalName(self):
        self.localname = self.doc.CURFILE.split('/')
        return "Current File: " + self.localname[len(self.localname) - 1]

    def updateBoxes(self):

        ##########################
        # file box
        self.curFileBox.config(state=tk.NORMAL)
        self.curFileBox.delete(1.0, tk.END)
        curfile = self.getLocalName()
        self.curFileBox.insert(1.0, curfile)
        self.curFileBox.config(state=tk.DISABLED)
        ##########################
        # print(len(self.linesDict))
        print(len(self.keys))
        print(self.curfunccounter)
        t = self.keys[self.curfunccounter]
        funcstr = self.linesDict[t]
        # print("funcstr is: " + funcstr)
        ##########################
        # function box
        self.functionbox.config(state=tk.NORMAL)
        self.functionbox.delete(1.0, tk.END)
        self.functionbox.insert(1.0, funcstr)    #"test" + str(self.curfunccounter))
        self.functionbox.config(state=tk.DISABLED)
        ##########################
        # print("current count: " + str(self.curfunccounter))

        ##########################
        # comment box
        self.commentbox.delete(1.0, tk.END)
        if self.keys[self.curfunccounter] in self.comments:
            self.commentbox.insert(1.0, self.comments[self.keys[self.curfunccounter]])
            # print(self.comments[self.keys[self.curfunccounter]])
        else:
            self.commentbox.insert(1.0, self.langcom)
        # finally, call to remove newlines at end generated by insert
        self.removeNewlines()
        ##########################

