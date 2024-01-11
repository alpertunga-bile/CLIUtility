from subprocess import run
from platform import system
from sys import stdout
from os import remove, mkdir, getcwd
from re import compile
from os.path import join, exists
from logging import Logger, StreamHandler, Formatter, INFO
from json import load, dumps

# For coloring log outputs
class CustomFormatter(Formatter):
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        from logging import DEBUG, WARNING, ERROR, CRITICAL

        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            DEBUG: self.grey + self.fmt + self.reset,
            INFO: self.blue + self.fmt + self.reset,
            WARNING: self.yellow + self.fmt + self.reset,
            ERROR: self.red + self.fmt + self.reset,
            CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        logFormat = self.FORMATS.get(record.levelno)
        formatter = Formatter(logFormat)
        return formatter.format(record)


VENV_FILENAME = "venv"
VENVLOG_FILENAME = "venvLog.txt"
PATHS_FILENAME = "paths.json"
OS_NAME = system()
CURRENT_DIR = getcwd()

"""
Check functions
"""


def CheckPython(self) -> None:
    streamdata, isExist = self.RunCommand("python --version")

    if isExist:
        self.logger.info(f"Using {streamdata}")
    else:
        self.logger.error("Python is not exists")
        exit(1)


def CheckGit(self) -> bool:
    streamdata, isExist = self.RunCommand("git --version")

    if isExist:
        self.logger.info(f"Using {streamdata}")
    else:
        self.logger.error("Cant found git")

    return isExist


"""
Running Functions
"""


def CheckCommand(
    logger: Logger, terminalData: tuple, successMsg: str, failureMsg: str
) -> None:
    _, isSuccess = terminalData

    if isSuccess:
        logger.info(successMsg)
    else:
        logger.error(failureMsg)
        logger.error("ERROR OCCURED!!! Check venvLog file")
        exit(1)


def RunScript(logger: Logger, paths: dict, filename: str, args: str = "") -> None:
    script_filename = filename

    if filename.endswith(".py"):
        script_filename = script_filename[:-3]

    logger.info(
        f"Running {script_filename}.py with [{', '.join(args.split(' '))}] args"
    )
    command = f"{paths['python']} {script_filename}.py {args}"

    process = run(command, shell=True, check=True)

    if process.returncode == 0:
        logger.info(f"{script_filename}.py run successfully")
    else:
        logger.error(f"Cant run {script_filename}.py file")


def RunCommand(command: str, isCheck: bool = True) -> tuple:
    process = run(command, shell=True, check=isCheck, capture_output=True)

    streamdata = process.stdout
    streamdata = streamdata.decode("UTF-8")
    streamdata = streamdata.strip()

    with open(PATHS_FILENAME, "a") as file:
        if streamdata != "":
            file.write(f"{'-'*200}\n")
            file.write(f"Command : {command}\n")
            file.write(f"Output  :\n{streamdata}\n")

    return (streamdata, True) if process.returncode == 0 else (streamdata, False)


"""
Logger and envrionment functions
"""


def SetLogger(logger: Logger, loggerLevel) -> None:
    logger.setLevel(loggerLevel)

    handler = StreamHandler(stdout)
    handler.setLevel(INFO)
    logFormat = "[%(asctime)s] /_\ %(levelname)-8s /_\ %(message)s"
    if OS_NAME == "Windows":
        formatter = Formatter(logFormat)
    else:
        formatter = CustomFormatter(logFormat)

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def CreateEnv(logger: Logger):
    file = open(VENV_FILENAME, "w")
    file.close()
    logger.info(f"{VENVLOG_FILENAME} file is created")

    CheckPython()

    if exists(VENV_FILENAME):
        logger.info(f"Using {VENV_FILENAME} virtual environment")
    else:
        logger.info(f"Creating {VENV_FILENAME}")
        CheckCommand(
            RunCommand("python -m venv venv"),
            f"{VENV_FILENAME} is created",
            "Cant create virtual environment",
        )


def CreateRequirementsFile(paths: dict) -> None:
    command = f"{paths['pip']} freeze > requirements.txt"
    CheckCommand(
        RunCommand(command),
        "requirements.txt file is updated",
        "Cant create requirements file",
    )


def CheckPackages(logger: Logger, paths: dict, filename: str) -> tuple:
    logger.info("Checking Packages")
    command = f"{paths['pip']} freeze > temp_requirements.txt"
    RunCommand(command)

    envPackages = []
    with open("temp_requirements.txt", "r") as envFile:
        envPackages = set(envFile.readlines())

    # deleting the temp_requirements file
    remove("temp_requirements.txt")

    wantedPackages = []
    with open(filename, "r") as wantedFile:
        wantedPackages = set(wantedFile.readlines())

    # union function from set value type
    notIncludedPackages = wantedPackages - envPackages

    return (notIncludedPackages, wantedPackages.issubset(envPackages))


def InstallWRequirements(
    logger: Logger, paths: dict, filename: str = "requirements.txt"
) -> None:
    needToDownload, isContains = CheckPackages(filename)
    if isContains:
        logger.info("Requirements are already installed")
        return

    for package in needToDownload:
        package = package.strip()
        command = f"{paths['pip']} install {package}"
        logger.info(f"Installing {package}")
        RunCommand(command)

    CreateRequirementsFile()


"""
Path functions
"""


def GetPaths() -> dict:
    paths = {}

    if exists(PATHS_FILENAME):
        with open(PATHS_FILENAME, "r") as pathFile:
            paths = load(pathFile)

        for key, path in paths:
            if exists(path) is False:
                del paths[key]
    else:
        winPath = f"{VENV_FILENAME}\\Scripts"

        if OS_NAME == "Windows":
            paths["python"] = f"{winPath}\\python.exe"
            paths["pip"] = f"{winPath}\\pip.exe"
            paths["activate"] = f"{winPath}\\activate.bat"
            paths["deactivate"] = f"{winPath}\\deactivate.bat"
        elif OS_NAME == "Linux":
            paths["activate"] = f"source {VENV_FILENAME}/bin/activate"
            paths["python"] = f"{paths['activate']} && python3"
            paths["pip"] = f"{paths['activate']} && pip3"
            paths["deactivate"] = ""

    return paths


def SavePaths(paths: dict) -> None:
    with open(PATHS_FILENAME, "w") as file:
        jsonObject = dumps(paths, indent=4)
        file.write(jsonObject)


"""
Git functions
"""


def GetRepositoryName(repoLink: str) -> str:
    regexPattern = "([^/]+)\\.git$"
    pattern = compile(regexPattern)
    matcher = pattern.search(repoLink)
    return matcher.group(1)


def CloneRepository(
    logger: Logger, paths: dict, repoLink: str, repoKey: str, parentFolder: str = ""
) -> None:
    if CheckGit() is False:
        logger.error("Cannot detect git")
        return

    repoName = GetRepositoryName(repoLink)
    realRepoKey = repoKey + "-repo"

    if realRepoKey in paths.keys():
        logger.info(f"{repoName} is exists")
        return

    paths[realRepoKey] = join(parentFolder, repoName)
    SavePaths()

    if exists(join(CURRENT_DIR, parentFolder)) is False:
        mkdir(join(CURRENT_DIR, parentFolder))

    if parentFolder == "":
        command = f"git clone --recursive {repoLink}"
    else:
        command = (
            f"cd {parentFolder} && git clone --recursive {repoLink} && cd {CURRENT_DIR}"
        )

    logger.info(f"Cloning {repoLink}")
    RunCommand(command)


def UpdateRepository(logger: Logger, paths: dict, repoKey: str) -> None:
    if CheckGit() is False:
        logger.error("Cannot detect git")
        return

    realRepoKey = repoKey + "-repo"

    if realRepoKey not in paths.keys():
        logger.info(f"{repoKey} is not exists")
        return

    command = f"cd {paths[realRepoKey]} && git pull && cd {CURRENT_DIR}"

    logger.info(f"Updating {repoKey}")
    RunCommand(command)


def UpdateAllRepositories(logger: Logger, paths: dict) -> None:
    if CheckGit() is False:
        logger.error("Cannot detect git")
        return

    for key in paths.keys():
        if "-repo" not in key:
            continue

        UpdateRepository(key[:-5])


def RunScriptInsideRepository(
    logger: Logger, paths: dict, repoKey: str, repoCommand: str
) -> None:
    realRepoKey = repoKey + "-repo"

    if realRepoKey not in paths.keys():
        logger.info(f"{repoKey} is not exists")
        return

    command = ""
    if OS_NAME == "Windows":
        command = f"cd {paths[realRepoKey]} && {join(CURRENT_DIR, paths['python'])} {repoCommand} && cd {CURRENT_DIR}"
    elif OS_NAME == "Linux":
        command = f"{paths['activate']} && cd {paths[realRepoKey]} && python3 {repoCommand} && cd {CURRENT_DIR}"

    logger.info(f"Running {repoCommand}")
    RunCommand(command)


def InstallRequirementsFromRepository(
    logger: Logger, paths: dict, repoKey: str, file: str = "requirements.txt"
) -> None:
    realRepoKey = repoKey + "-repo"

    if realRepoKey not in paths.keys():
        logger.info(f"{repoKey} is not exists")
        return

    InstallWRequirements(join(paths[realRepoKey], file))


def InstallRequirementsFromAllRepositories(logger: Logger, paths: dict) -> None:
    if CheckGit() is False:
        logger.error("Cannot detect git")
        return

    for key in paths.keys():
        if "-repo" not in key:
            continue

        InstallRequirementsFromRepository(key[:-5])
