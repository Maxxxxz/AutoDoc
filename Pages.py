import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Page(tk.Frame):
    def __init__(self):
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
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, '\n'.join(self.selectedFiles))
        self.textbox.config(state=tk.DISABLED)

    def langSelectEvent(self, event, argu):
        self.SELECTED = argu.get()
        print(self.SELECTED)

#   Documentor pages
class DocumenterPage(Page):
    def __init__(self, w, h):
        Page.__init__(self)

        ##########################
        #   Show the current Function
        self.functionbox = tk.Text(self)
        self.functionbox.config(width=50, height=1) # 1 line tall, 50 chars long
        self.functionbox.place(x=(w/2), y=((h/2) - (h/2.25)), anchor="center")
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

    def but_nextFunc(self):
        print("next func")

    def but_noDoc(self):
        print("no documentation!")
        print(self.FILES)

    def but_prevFunc(self):
        print("prev func")
