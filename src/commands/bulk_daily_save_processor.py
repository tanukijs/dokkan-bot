import os
import sys

import config
from commands.accept_gifts import accept_gifts_command
from commands.accept_missions import accept_missions_command
from commands.complete_potential import complete_potential_command
from commands.complete_stage import complete_stage_command
from commands.daily_login import daily_login_command
from commands.refresh_client import refresh_client_command
from commands.user_command_executor import user_command_executor_command


def bulk_daily_save_processor_command(save, login, gift, daily_events, user_input):
    f = open(os.path.join(save), 'r')
    config.identifier = f.readline().rstrip()
    config.AdId = f.readline().rstrip()
    config.UniqueId = f.readline().rstrip()
    config.platform = f.readline().rstrip()
    config.client = f.readline().rstrip()
    f.close()

    try:
        refresh_client_command()
    except:
        print('Sign in failed' + save)
        return 0

    ###
    if login == True:
        daily_login_command()
    if gift == True:
        accept_gifts_command()
    if daily_events == True:
        complete_stage_command('130001', 0)
        complete_stage_command('131001', 0)
        complete_stage_command('132001', 0)
        complete_potential_command()
        accept_gifts_command()
        accept_missions_command()
        print('Completed Daily Grind')
    while len(user_input) > 1:
        user_command_executor_command(user_input)
        try:
            user_input = input()
        except:
            sys.stdin = sys.__stdin__
            break
