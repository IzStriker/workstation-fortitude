import fileinput
import re

from workstationfortitude.optonnotfound import OptionNotFound
def get_option(option: str, file: str):
    try:
        with open(file, "r") as file:
            config = file.read()
            option = option.replace(".", "\\.")
            regex ='^' + option + '\\s*=\\s*\\"(.+)\\"$'
            res = re.search(regex, config, re.MULTILINE)
            return res.group(1)
    except FileNotFoundError:
        raise
    except Exception:
        raise OptionNotFound(option)

def set_option(option: str, value: str, filename: str):
    regex = option.replace(".", "\\.") + '\\s*=\\s*\\".*\\"'
    pattern = re.compile(regex)
    option_set = False
    try:
        with fileinput.FileInput(filename, inplace=True) as file:
            for line in file:
                if pattern.match(line) != None:
                    print(f'{option} = "{value}"')
                    option_set = True
                else:
                    print(line, end = "")
    except:
        raise
    if not option_set:
        raise OptionNotFound(option)

def add_option(option: str, value: str, filename: str):
    try:
        with open(filename, "a") as file:
            file.write(f'\n{option} = "{value}"')
    except:
        raise

