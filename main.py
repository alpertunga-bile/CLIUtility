from Loader import Loader
from VenvManager import VenvManager
from Completer import Completer

if __name__ == "__main__":
    tempDict = {"Physics":43, "Math":23}
    for key, value in Loader(tempDict.items(), description="Test"):
        pass