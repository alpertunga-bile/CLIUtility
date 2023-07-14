# CLIUtility

- Providing some utility classes for CLI applications.

## Utilities
### Loader Class
- Providing loader for CLI like tqdm package.
- You can use it with range, list, tuple, set and dict data types.
- Can specify description and loading char to visualize.
#### Example For Range
```python
for i in Loader(range(1, 10), description="Test"):
        pass
```
#### Example For List, Set And Tuple
```python
tempList = ["10", "2", "5"]
for i in Loader(tempList, description="Test"):
        pass
```
#### Example For Dictionary
```python
tempDict = {"Physics":43, "Math":23}
for key, value in Loader(tempDict.items(), description="Test"):
        pass
```
#### Example Result
```Test [####################################################################################################] %100```
### Completer Class
- Providing tab completer for CLI.
- You can specify your completer functions with words.
- You can use it for get files and folders for given directory or current directory.
### VenvManager Class
You can
- Create virtual environment
- Install packages with requirements file
- Run scripts with args
- Clone repository
- Update repository
- Install requirements from repository
- Run scripts from repository
