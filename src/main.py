import sys

import requests
from colorama import Fore, Style, init

import config
from classes.Game import GameEnvironment, GameAccount
from commands.auth.db_download import db_download_command
from commands.auth.load_account import load_account_command
from commands.auth.save_account import save_account_command
from commands.auth.signin import signin_command
from commands.auth.signup import signup_command
from commands.auth.transfer_account import transfer_account_command
from commands.game.accept_gifts import accept_gifts_command
from commands.game.accept_missions import accept_missions_command
from commands.game.bulk_daily_logins import bulk_daily_logins_command
from commands.game.daily_login import daily_login_command
from commands.game.tutorial import tutorial_command
from user_command_executor import user_command_executor_command

init(autoreset=True)

# before anything a request for new URL & API port is required. - k1mpl0s
def check_servers(env: GameEnvironment):
  try:
    url = env.url + '/ping'
    # we send an ancient version code that is valid.
    headers = {
      'X-Platform': 'android',
      'X-ClientVersion': env.version_code,
      'X-Language': 'en',
      'X-UserID': '////'
    }
    r = requests.get(url, data=None, headers=headers)
    # store our requested data into a variable as json.
    store = r.json()
    print(store)
    if 'error' in store:
      print(Fore.RED + '[' + env.name + ' server] ' + str(store['error']))
      return False
  except:
    print(Fore.RED + '[' + env.name + ' server] can\'t connect.')
    return False
  return True;


def check_database():
  print(' ')
  print(Fore.CYAN + Style.BRIGHT + 'Select one of the following')
  print('---------------------------------')
  print(' ')
  # Database Check.
  while True:
    print(
      'Check for updated database? (' + Fore.YELLOW + Style.BRIGHT + 'Yes: 1 ' + Style.RESET_ALL + 'or ' + Fore.YELLOW + Style.BRIGHT + 'No: 2' + Style.RESET_ALL + ')',
      end='')
    db = input(' ')
    if db.lower() == '1':
      db_download_command()
      break
    elif db.lower() == '2':
      break
    else:
      print('')
      continue


def daily_logins():
  # Daily Logins?
  print(' ')
  print(Fore.CYAN + Style.BRIGHT + 'Choose an option')
  print('---------------------------------')
  print(' ')
  while True:
    print(
      'Perform daily logins on all accounts? (' + Fore.YELLOW + Style.BRIGHT + 'Yes: 1 ' + Style.RESET_ALL + 'or ' + Fore.YELLOW + Style.BRIGHT + 'No: 2' + Style.RESET_ALL + ')',
      end='')
    db = input(' ')
    if db.lower() == '1':
      bulk_daily_logins_command()
      break
    elif db.lower() == '2':
      break
    else:
      continue


def choose_client():
  # Decide which client to use.
  print(' ')
  print(Fore.CYAN + Style.BRIGHT + 'Choose a version')
  print('---------------------------------')
  print(' ')
  while True:
    print(
      'Which version? (' + Fore.YELLOW + Style.BRIGHT + 'Jp: 1 ' + Style.RESET_ALL + 'or ' + Fore.YELLOW + Style.BRIGHT + 'Global: 2' + Style.RESET_ALL + ')',
      end='')
    choose = input(" ")
    if choose.lower() == '1':
      config.game_env = config.JP_ENV
      break
    elif choose.lower() == '2':
      config.game_env = config.GB_ENV
      break
    else:
      continue


if check_servers(config.game_env):
  print(Fore.GREEN + 'connected successfully.')
else:
  # we can't use the farmbot period if there's no URL to make requests to...
  print(Fore.RED + 'press ENTER to close...')
  input()
  exit()

while True:
  check_database()
  daily_logins()
  choose_client()

  command = ''
  config.reroll_state = False

  while command != 'exit':
    # User Options
    print(' ')
    if command == 'reroll' or command == '':
      while True:
        if config.reroll_state:
          command = '0'
        else:
          print('---------------------------------')
          print(Fore.CYAN + Style.BRIGHT + 'New Account :' + Fore.YELLOW + Style.BRIGHT + ' 0')
          print(Fore.CYAN + Style.BRIGHT + 'Transfer Account :' + Fore.YELLOW + Style.BRIGHT + ' 1')
          print(Fore.CYAN + Style.BRIGHT + 'Load From Save :' + Fore.YELLOW + Style.BRIGHT + ' 2')
          print(Fore.CYAN + Style.BRIGHT + 'Load From Identifier :' + Fore.YELLOW + Style.BRIGHT + ' 3')
          print('---------------------------------')
          command = input('Enter your choice: ')
          config.reroll_state = False
        if command == '0':
          print(' ')
          config.game_account = signup_command(config.reroll_state)
          save_account_command(config.reroll_state)
          access_token, secret = signin_command(config.game_account.identifier)
          config.game_account.access_token = access_token
          config.game_account.secret = secret
          tutorial_command()
          daily_login_command()
          if config.reroll_state:
            accept_gifts_command()
            accept_missions_command()
            print(' ')
            print(' --------- Alright guys! We\'re back for another Dokkan Battle Video! ---------- ')
            print(' ')
            user_command_executor_command('summon')
          break
        elif command == '1':
          print(' ')
          transfer_account_command()
          daily_login_command()
          break
        elif command == '2':
          print(' ')
          load_account_command()
          daily_login_command()
          accept_gifts_command()
          accept_missions_command()
          break
        elif command == '3':
          print(' ')
          print(Fore.CYAN + Style.BRIGHT + 'Enter identifier below...')
          config.game_account = GameAccount(
            identifier=input()
          )
          save_account_command(config.reroll_state)
          access_token, secret = signin_command(config.game_account.identifier)
          config.game_account.access_token = access_token
          config.game_account.secret = secret
          daily_login_command()
          accept_gifts_command()
          accept_missions_command()
          break
        else:
          print(Fore.RED + Style.BRIGHT + "Command not understood")

    # User commands.
    while True:
      print('---------------------------------')
      print(
        Fore.CYAN + Style.BRIGHT + "Type" + Fore.YELLOW + Style.BRIGHT + " 'help'" + Fore.CYAN + Style.BRIGHT + " to view all commands.")

      # Set up comma separated chain commands. Handled via stdin
      try:
        command = input()
      except:
        sys.stdin = sys.__stdin__
        command = input()

      if command == 'exit':
        config.reroll_state = False
        break
      elif command == 'reroll':
        config.reroll_state = True
        break

      # Pass command to command executor and handle keyboard interrupts.
      try:
        user_command_executor_command(command)
      except KeyboardInterrupt:
        print(Fore.CYAN + Style.BRIGHT + 'User interrupted process.')
      except Exception as e:
        print(Fore.RED + Style.BRIGHT + repr(e))
