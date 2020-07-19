import os
import Documenter as dc

# Move regex loading to Documenter.py to avoid duplicate code
class CLI():

    self.files = []
    self.doc = None
    self.lang = None
    self.regex = None

    def runCLI():
        # print("You will now be asked for the ")
        print("Input File Names (relative or absolute). Type 'done' to finish inputting files.")
        print("Prepend with -r to remove the specified file.")
        print("Use -list to list currently selected files.")
        # use input to grab relative or absolute path
        # print(os.getcwd())
        fin = False

        while not fin:
            inp = input("Path: ")
            if inp == "done":
                fin = True
            elif inp == "-list":
                print("Currently Selected Files:")
                for file in files:
                    print(file)
            elif inp.startswith("-r"):
                inp = os.path.realpath(inp[3:])
                if inp in files:
                    files.remove(inp)
                else:
                    print("File: {} not in list.".format(inp))
            else:
                if os.path.exists(inp):
                    inp = os.path.realpath(inp)
                    if inp in files:
                        print("File: {} already in list.".format(inp))
                    else:
                        files.append(inp)
                else:
                    print("File: {} not found".format(inp))

        print("The following files will be used as input:\n{}".format(("\n".join(files))))

        self.doc = dc.Documenter("Python", files, "*", None)

