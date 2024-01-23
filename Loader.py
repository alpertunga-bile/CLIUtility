from collections.abc import KeysView, ItemsView
import time
from sys import stdout


class Loader:
    desc: str = ""
    start: int = -1
    end: int = -1
    step: int = 1
    counter: int = 0
    loadChar: str = "#"
    toAdd: int = 0
    iteration = None
    start_time = None
    end_time = None
    percentage = 0

    def SetValuesForRangeObject(
        self, givenRange: range, description: str, loadingChar: str
    ):
        if givenRange.start < 0 and givenRange.stop > 0:
            self.toAdd = -1 * givenRange.start
        elif givenRange.start < 0 and givenRange.stop < 0:
            self.toAdd = -1 * min(givenRange.start, givenRange.stop)

        self.iteration = iter(givenRange)
        self.SetAttributes(
            givenRange.start, givenRange.stop, givenRange.step, description, loadingChar
        )

    def SetAttributes(
        self, start: int, end: int, step: int, description: str, loadingChar: str
    ):
        self.start = start
        self.end = end - 1
        self.step = step
        self.counter = start
        self.desc = description
        self.loadChar = loadingChar

    def SetValuesForListTupleSetObjects(
        self, givenList: list, description: str, loadingChar: str
    ) -> None:
        self.iteration = iter(givenList)
        self.SetAttributes(0, len(givenList), 1, description, loadingChar)

    def __init__(self, iterableObject, description="Loader", loadingChar="#"):
        objectType = type(iterableObject)

        if objectType is range:
            self.SetValuesForRangeObject(iterableObject, description, loadingChar)
        elif objectType is list or objectType is tuple or objectType is set:
            self.SetValuesForListTupleSetObjects(
                iterableObject, description, loadingChar
            )
        elif isinstance(iterableObject, KeysView) or isinstance(
            iterableObject, ItemsView
        ):
            tempList = list(iterableObject)
            self.SetValuesForListTupleSetObjects(tempList, description, loadingChar)
        else:
            print(f"{objectType} for iterableObjects is not supported")
            exit(0)

    def __iter__(self):
        self.Update(True)
        self.PrintBar(0.0)
        self.counter = self.start - 1
        self.start_time = time.time()
        self.end_time = time.time()
        return self

    def __next__(self):
        self.counter = self.counter + self.step
        if self.counter <= self.end:
            self.Update(False)
            self.end_time = time.time()
            self.PrintBar(self.end_time - self.start_time)
            self.start_time = time.time()
            return next(self.iteration)
        else:
            self.Update(True)
            self.PrintBar(0.0)
            print("\n")
            raise StopIteration

    def PrintBar(self, eta: float) -> None:
        remains = 100 - self.percentage

        total_seconds = eta * float(remains)

        remain_hours = total_seconds / 3600.0
        total_seconds -= float(int(remain_hours)) * 3600.0

        remain_minutes = total_seconds / 60.0
        total_seconds -= float(int(remain_minutes)) * 60.0

        remain_seconds = total_seconds

        loadStr = "\r" + self.desc + " ["
        loadStr += self.loadChar * self.percentage
        loadStr += " " * remains
        loadStr += f"] %{self.percentage} ETA [{int(remain_hours):3} h| {int(remain_minutes):3} m| {remain_seconds:3.2f} s]  "
        print(loadStr, end="")
        stdout.flush()

    def Update(self, empty: bool = False):
        start_point = float(self.counter + self.toAdd)
        end_point = float(self.end + self.toAdd if self.end + self.toAdd > 0 else 1.0)
        percentage = int((start_point / end_point) * 100.0) if end_point != 1.0 else 100

        if empty:
            percentage = 100

        self.percentage = percentage
