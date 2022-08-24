import traceback

from colorama import Fore

import commands
import config
from services.command import CommandService


def execute(user_input: str):
    for command_name in CommandService.get_names():
        command = CommandService.get_all()[command_name]
        is_current = user_input.startswith(command_name)
        if not is_current or config.game_context not in command.CONTEXT: continue

        raw_args = user_input.removeprefix(command_name).strip()
        command_args = [arg for arg in raw_args.split(' ') if arg]
        try:
            command.run(*command_args)
            break
        except TypeError as error:
            print('invalid command arguments: ', command_args)
            print(error)
        except Exception as error:
            print('command error')
            traceback.print_exc()
            print(error)


def run():
    print(Fore.GREEN + 'Welcome to Dokkan 777')
    CommandService.load()
    commands.help.run()

    while True:
        user_input = input(Fore.YELLOW + '777 $ ' + Fore.RESET).strip()
        execute(user_input)

# OMEGA Command
#   accept_gifts_command()
#   accept_missions_command()
#   complete_unfinished_quest_stages_command()
#   complete_unfinished_events_command()
#   complete_unfinished_zbattles_command()
#   complete_clash_command()

# Daily Command
#   complete_stage_command('130001', 0)
#   complete_stage_command('131001', 0)
#   complete_stage_command('132001', 0)
#   complete_potential_command()
#   accept_gifts_command()
#   accept_missions_command()
