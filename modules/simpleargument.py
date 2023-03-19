import json
import re
from typing import Callable

def trigger_func():
    return True

class SimpleArguments:
    """
    A class that helps to parse and handle simple arguments from user input text.

    Attributes:
        args (dict): A dictionary to store the arguments and their corresponding values.

    Methods:
        get_argument(name: str) -> Any:
            Returns the value of an argument given its name. If the argument is not found, returns False.

        set_argument(name: str, callback: Callable) -> None:
            Sets a callback function to be called when an argument with the specified name is encountered.

        parser(text: str) -> None:
            Parses the input text and sets the corresponding arguments and their values in the `args` dictionary.
            If an argument has a callback function associated with it, the function is called when the argument is parsed.
    """
    def __init__(self) -> None:
        """
        Initializes a new instance of the SimpleArguments class with an empty dictionary to store the arguments.
        """
        self.args = {}
    def get_argument(self, name : str):
        """
        Returns the value of an argument given its name. If the argument is not found, returns False.

        Args:
            name (str): The name of the argument to retrieve.

        Returns:
            Any: The value of the argument, or False if the argument is not found.
        """

        if name in self.args:
            return self.args[name]
        
        return False
    
    def set_argument(self, name : str, callback : Callable):
        """
        Sets a callback function to be called when an argument with the specified name is encountered.

        Args:
            name (str): The name of the argument to set the callback function for.
            callback (Callable): The callback function to be called when the argument is encountered.
        """
        self.args[name] = callback

    def clear(self):
        """
        Remove all arguments.
        """
        self.args = {}
    @staticmethod
    def print_help(path : str):
        """
        Print all arguments with info.
        """
        with open(path, 'r') as f:
            helps : dict = json.loads(f.read())
        print("Welcome to Simple Arguments!")
        print("Arguments:")

        for key, h in helps.items():
            if str(key).startswith("_"):
                print("\t", f'{str(key).replace("_", "")}={str(key).replace("_", "").upper()}', ":", h)
            else:
                print("\t", str(key), ":", h)
        
        return
    def parser(self, text : str):
        """
        Parses the input text and sets the corresponding arguments and their values in the `args` dictionary.
        If an argument has a callback function associated with it, the function is called when the argument is parsed.

        Args:
            text (str): The text to be parsed for arguments.
        """
        
        pattern = r'\b(\w+)\s*=\s*["\']?([^"\']+)'
        matches = re.findall(pattern, text)

        for match in matches:
            key = match[0]
            value = match[1]
            self.args[key.replace(" ", "")] = value
            text = text.replace(f'{key}="{value}"', "")

        actions = text.split(" ")
        for action in actions:
            if action == "" or action is None:
                continue
            self.args[action.replace(" ", "")] = trigger_func


if __name__ == "__main__":
    sa = SimpleArguments()
    sa.parser('"sub saveto=\"mydir\""')

    print(sa.args)