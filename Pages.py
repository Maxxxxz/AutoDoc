import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import Documenter as dc
from typing import List

# Add self.approot variable so all child pages have direct access to the app root
class Page(tk.Frame):
    def __init__(self):
        self.LANG = None
        self.FILES = None
        tk.Frame.__init__(self)

    def show(self, event=None):
        self.lift()

    def setLang(self, lang):
        self.LANG = lang

    def setFiles(self, files):
        self.FILES = files

#   Main menu
class Menu(Page):
    def __init__(self, w, h):
        Page.__init__(self)
        #label = tk.Label(self, text="Python Template Window")
        #label.place(x=(w/2), y=25, anchor="center")  # Place label at top of screen
        self.SELECTED = None    #init SELECTED var
        self.selectedFiles = None
        ###############################
        #   Language Selection Combobox
        self.cb = ttk.Combobox(self, textvariable=tk.StringVar(),
                       values=["Python", "C++", "C", "Ruby", "C#", "Go", "Java", "Javascript"
                           , "PHP", "Kotlin", "Scala", "Haskell", "Lua", "Rust", "Perl"],
                       state="readonly")  # Drop down menu
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

    def openFiles(self):
        self.selectedFiles = filedialog.askopenfilenames(title="Select files")
        self.textbox.config(state=tk.NORMAL)
        self.textbox.delete('1.0', tk.END)  # strange behaviour when not using '1.0'
        self.textbox.insert(tk.END, '\n'.join(self.selectedFiles))
        self.textbox.config(state=tk.DISABLED)
        if self.selectedFiles is not None:
            self.master.children["!application"].setContent(self.SELECTED, self.selectedFiles)

    def langSelectEvent(self, event, argu):
        self.LANG = argu.get()
        self.master.children["!application"].setContent(argu.get(), self.selectedFiles)

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
        #   Initialize variables
        self.curfunccounter = 0
        self.linesDict: dict
        self.comments: List = []
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
        self.commentbox.insert(tk.END, "test!")
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
        self.doc = dc.Documenter(self.LANG, self.FILES)
        # initial page content put in here
        # self.linesDict = self.doc.getLines()

    # need to add keys to the self.comments so I can pass that to comment
    def but_nextFunc(self):
        somevar = False
        if somevar:    # if no more functions in file to document
            t_choice = messagebox.askyesno("Confirm Documentation of File", "Are you sure you want to add documentation to this file?")
            if t_choice:    # if yes: add documentation
                self.doc.comment(self.comments)
            else:   # else just do nothing, lets the user go back and change their info
                pass
        else:       # else just do logic to move onto next function
            if len(self.comments) >= (self.curfunccounter + 1):  # if index already exists (index + 1) override current comment at index
                self.comments[self.curfunccounter] = self.commentbox.get('1.0', tk.END)
            else:  # else: append current comment and increment counter
                self.comments.append((self.commentbox.get('1.0', tk.END)).split('\n'))

            self.curfunccounter += 1

        # now show the next function
        self.updateBoxes()

        # print("next func")

    def but_noDoc(self):
        self.commentbox.edit_reset()    # make the comment box empty
        self.but_nextFunc() # just call nextFunc logic, it is the same when the comment box is entirely empty
        # print("no documentation!")

    def but_prevFunc(self):
        if len(self.comments) >= (self.curfunccounter + 1):  # if index already exists (index + 1) override current comment at index
            self.comments[self.curfunccounter] = self.commentbox.get('1.0', tk.END)
        else:  # else: append current comment and decrement counter
            self.comments.append(self.commentbox.get('1.0', tk.END))

        self.curfunccounter -= 1

        # now show the previous function

        self.updateBoxes()

        # print("prev func")

    def updateBoxes(self):
        self.functionbox.config(state=tk.NORMAL)
        self.functionbox.delete('1.0', tk.END)
        self.functionbox.insert('1.0', "test" + str(self.curfunccounter))
        self.functionbox.config(state=tk.DISABLED)
        # print("current count: " + str(self.curfunccounter))
