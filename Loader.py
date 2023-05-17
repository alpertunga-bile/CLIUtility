import sys

class Loader:
    desc = ""
    start = -1
    end = -1
    step = 1
    counter = 0
    loadChar = '#'

    def __init__(self, range : range, description="Loader", loadingChar="#"):
        if range.start < 0:
            oneMinusMulStart = -1 * range.start
            self.start = 0
            self.end = range.stop + oneMinusMulStart
        else:
            self.start = range.start
            self.end = range.stop

        self.step = range.step
        self.counter = range.start
        self.desc = description
        self.loadChar = loadingChar

    def __iter__(self):
        self.counter = self.start
        self.Update()
        return self
    
    def RemoveLastLine(self):
        sys.stdout.write('\x1b[1A') 
        sys.stdout.write('\x1b[2K')
    
    def __next__(self):
        if self.counter <= self.end:
            self.RemoveLastLine()
            self.Update()
            self.counter = self.counter + self.step
            return self.counter
        else:
            raise StopIteration

    def Update(self):
        percentage = int((float(self.counter) / float(self.end)) * 100.0)
        loadStr = self.desc + " ["
        loadStr += self.loadChar * percentage
        loadStr += " " * (100 - percentage)
        loadStr += f"] %{percentage}"
        print(loadStr)