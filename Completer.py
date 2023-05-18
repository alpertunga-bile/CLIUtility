from readline import parse_and_bind, set_completer, get_completer

class CompleteFunction:
    vocabs : list = None
    completeFunc = None

    def __init__(self, completeFunc = None, vocabs = None):
        self.vocabs = vocabs
        self.completeFunc = completeFunc

    def Completer(self, text, state):
        results = [x for x in self.vocabs if x.startswith(text)] + [None]
        return results[state]
    
    def GetCompleter(self):
        if self.vocabs is None:
            return self.completeFunc
        else:
            return self.Completer

class Completer:
    completeDict = {}

    def __init__(self):
        parse_and_bind("tab: complete")

    def AddCompleteFunction(self, name, func):
        completeFunc = CompleteFunction(func)
        self.completeDict[name] = completeFunc

    def GetCompleteFunction(self, name):
        return self.completeDict[name]
    
    def DeleteCompleteFunction(self, name):
        if self.completeDict[name]:
            del self.completeDict[name]

    def CreateCompleteFunction(self, name, vocabs : list):
        completeFunc = CompleteFunction(completeFunc=None, vocabs=vocabs)
        self.completeDict[name] = completeFunc

    def SetCompleteFunction(self, name):
        if self.completeDict[name]:
            set_completer(self.completeDict[name].GetCompleter())

    def SetDefaultCompleteFunction(self):
        set_completer(None)

    def GetCurrentCompleteFunction(self):
        return get_completer()