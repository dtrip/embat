import os

class Output:
    f = None

    def __init__(self):
        pass

    def createFile(self, outputFile):

        if (os.path.exists(outputFile)):
            # opens file if exists and appends to it
            Output.f = open(outputFile, "a+")
        else:
            Output.f = file(outputFile, "w")
            self.__initFileSetup()
        return Output.f

    def __initFileSetup(self):
        Output.f.write("Email Address, Password\n")
        return True

    def addRow(self, email, pw):
        Output.f.write(email + ", " + pw + "\n")
        return True
