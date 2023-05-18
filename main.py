from Loader import Loader
from StartManager import StartManager
from Completer import Completer

if __name__ == "__main__":
    completer = Completer()
    completeName = "yesno"
    completeVocabs = ["yes", "no"]
    completer.CreateCompleteFunction(completeName, completeVocabs)
    completer.SetCompleteFunction(completeName)
    test = input("Enter something : ")