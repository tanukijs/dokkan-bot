import importlib
from inspect import getmembers
from types import ModuleType

from colorama import Fore, Style

import commands
import pkgutil


class CommandService:
    __commands = {}

    @staticmethod
    def load():
        modules = pkgutil.iter_modules(commands.__path__, commands.__name__ + '.')
        for module in modules:
            try:
                command = importlib.import_module(module.name)
                is_valid = CommandService.is_valid(command)
                if not is_valid: continue
                CommandService.__commands[command.NAME] = command
            except ImportError as e:
                print(f'[{Fore.RED}ImportError{Fore.RESET}] {e}')

    @staticmethod
    def is_valid(module: ModuleType) -> bool:
        constants = ['NAME', 'DESCRIPTION', 'CONTEXT']
        methods = ['run']
        members = [*constants, *methods]
        module_member_names = [name for name, value in getmembers(module)]
        missing_member_names = [name for name in members if name not in module_member_names]
        if len(missing_member_names) > 0:
            attributes = ', '.join(map(lambda k: f'\033[4m{k}{Style.RESET_ALL}', missing_member_names))
            print(f'[{Fore.RED}AttributeError{Fore.RESET}] Missing attributes {attributes} in {module.__name__}')
            return False

        return True

    @staticmethod
    def get_all() -> dict:
        return CommandService.__commands

    @staticmethod
    def get_names() -> list[str]:
        names = list(CommandService.__commands.keys())
        names.sort(key=lambda name: len(name), reverse=True)
        return names
