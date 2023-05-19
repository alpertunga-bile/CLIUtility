from Loader import Loader
from VenvManager import VenvManager
from Completer import Completer

if __name__ == "__main__":
    file = open("test.txt", "w")

    randomDict = {'Physics':67, 'Maths':87, 'Wololo':234}
    
    for key, value in Loader(randomDict.items(), "Test"):
        file.write(f"{key} ==> {value}\n")

    file.close()