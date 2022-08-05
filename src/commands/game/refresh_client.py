from colorama import Fore, Style

import config
from commands.auth.signin import signin_command


def refresh_client_command():
  config.access_token, config.secret = signin_command(config.identifier)
  print(Fore.GREEN + Style.BRIGHT + 'Refreshed Token')
