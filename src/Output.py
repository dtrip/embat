import os
from colorama import init, Fore, Back, Style

class Output:
    f = None

    def __init__(self):
        pass

    def createFile(self, outputFile):

        try:
            if (os.path.exists(outputFile)):
                # opens file if exists and appends to it
                Output.f = open(outputFile, "w")
            else:
                Output.f = file(outputFile, "w")
                self.__initFileSetup()
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + "[-] Error: " + str(e) + Style.RESET_ALL)
        return Output.f

    def __initFileSetup(self):
        Output.f.write("Email Address, Password\n")
        print("output file has been initiated")
        return True

    def addRow(self, email, pw):
        Output.f.write(email + ", " + pw + "\n")
        return True
