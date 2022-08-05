from colorama import Fore, Style

import config
from commands.auth.signin import signin_command


def refresh_client_command():
  access_token, secret = signin_command(config.game_account.identifier)
  config.game_account.access_token = access_token
  config.game_account.secret = secret
  print(Fore.GREEN + Style.BRIGHT + 'Refreshed Token')
