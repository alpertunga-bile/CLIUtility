from subprocess import run, DEVNULL
from platform import system
from sys import stdout
from os.path import join, exists
from logging import getLogger, Logger, StreamHandler, Formatter, INFO, DEBUG

class VenvManager:
    opsys : str
    venvName : str
    paths : dict
    logger : Logger

    def __init__(self, envName : str ="venv", loggerLevel=INFO):
        self.venvName = envName
        self.opsys = system()
        self.paths = {}

        self.logger = getLogger()
        self.logger.setLevel(loggerLevel)
        handler = StreamHandler(stdout)
        handler.setLevel(INFO)
        formatter = Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        winPath = f"{envName}\\Scripts"

        if self.opsys == "Windows":
            self.paths["python"] = f"{winPath}\\python.exe"
            self.paths["pip"] = f"{winPath}\\pip.exe"
            self.paths["activate"] = f"{winPath}\\activate.bat"
            self.paths["deactivate"] = f"{winPath}\\deactivate.bat"
        elif self.opsys == "Linux":
            self.paths["python"] = "python3"
            self.paths["pip"] = "pip3"
            self.paths["activate"] = f"source {envName}/bin/activate"
            self.paths["deactivate"] = ""

        self.logger.log(DEBUG, self.paths.__str__())

        self.logger.log(INFO, "VenvLog file is created")
        file = open("venvLog.txt", "w")
        file.close()

        if exists(envName):
            self.logger.log(INFO)

        self.logger.log(INFO, f"Creating {envName}")
        self.RunCommand("python -m venv venv")

    def RunCommand(self, command : str) -> bool:
        with open("venvLog.txt", "a") as file:
            returnCode = run(command, shell=True, stderr=file, stdout=file)

        return True if returnCode == 0 else False
