import sys
from collections.abc import KeysView, ItemsView

class Loader:
    desc = ""
    start = -1
    end = -1
    step = 1
    counter = 0
    loadChar = '#'
    toAdd = 0
    iteration = None

    def SetValuesForRangeObject(self, givenRange : range, description : str, loadingChar : str):
        if givenRange.start < 0 and givenRange.stop > 0:
            self.toAdd = -1 * givenRange.start
        elif givenRange.start < 0 and givenRange.stop < 0:
            self.toAdd = -1 * min(givenRange.start, givenRange.stop)
    
        self.iteration = iter(givenRange)
        self.SetAttributes(givenRange.start, givenRange.stop, givenRange.step, description, loadingChar)

    def SetValuesForListTupleSetObjects(self, givenList : list, description : str, loadingChar : str):
        self.iteration = iter(givenList)
        self.SetAttributes(0, len(givenList), 1, description, loadingChar)

    def __init__(self, iterableObject, description="Loader", loadingChar="#"):
        objectType = type(iterableObject)
        
        if objectType is range:
            self.SetValuesForRangeObject(iterableObject, description, loadingChar)
        elif objectType is list or objectType is tuple or objectType is set:
            self.SetValuesForListTupleSetObjects(iterableObject, description, loadingChar)
        elif isinstance(iterableObject, KeysView) or isinstance(iterableObject, ItemsView):
            tempList = list(iterableObject)
            self.SetValuesForListTupleSetObjects(tempList, description, loadingChar)
        else:
            print(f"{objectType} for iterableObjects is not supported")
            exit(0)

    def SetAttributes(self, start : int, end : int, step : int, description : str, loadingChar : str):
        self.start = start
        self.end = end - 1
        self.step = step
        self.counter = start
        self.desc = description
        self.loadChar = loadingChar

    def __iter__(self):
        self.Update()
        self.counter = self.start - 1
        return self
    
    def RemoveLastLine(self):
        sys.stdout.write('\x1b[1A') 
        sys.stdout.write('\x1b[2K')
    
    def __next__(self):
        self.counter = self.counter + self.step
        if self.counter <= self.end:
            self.RemoveLastLine()
            self.Update()
            return next(self.iteration)
        else:
            raise StopIteration

    def Update(self):
        percentage = int((float(self.counter + self.toAdd) / float(self.end + self.toAdd)) * 100.0)
        loadStr = self.desc + " ["
        loadStr += self.loadChar * percentage
        loadStr += " " * (100 - percentage)
        loadStr += f"] %{percentage}"
        print(loadStr)