from Loader import Loader
from VenvManager import VenvManager
from Completer import Completer

if __name__ == "__main__":
    venvManager = VenvManager("venv")

    completer = Completer()
    completeName = "yesno"
    completeVocabs = ["yes", "no"]
    completer.CreateCompleteFunction(completeName, completeVocabs)
    completer.CreateCurrentDirectoryFilesCompleteFunction("currentDir")
    completer.SetCompleteFunction(completeName)
    test = input("Enter something : ")
    completer.SetCompleteFunction("currentDir")
    test = input("Enter something : ")