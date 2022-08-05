import os
from random import randint

import config
import requests
from colorama import Fore, Style
from commands.auth.signin import signin_command
from commands.auth.signup import signup_command
from network.utils import generate_headers
from pysqlsimplecipher.decryptor import decrypt_file


def db_download_command():
  config.game_env.db_path.parent.mkdir(exist_ok=True, parents=True)
  glb_out_of_date = False

  # Check local DB versions in help.txt
  while True:
    if os.path.isfile('help.txt'):
      f = open(os.path.join('help.txt'), 'r')
      local_version_glb = f.readline().rstrip()
      f.close()
      break
    else:
      f = open(os.path.join('help.txt'), 'w')
      f.write('111\n')
      f.close()

  # Set first db to download to global.
  config.identifier = signup_command(False)
  config.access_token, config.secret = signin_command(config.identifier)

  headers = generate_headers('GET', '/client_assets/database')
  url = config.game_env.url + '/client_assets/database'
  r = requests.get(url, allow_redirects=True, headers=headers)
  temp_db_name = str(randint(10_000_00, 99_999_99)) + '.db'

  if local_version_glb != str(r.json()['version']):
    glb_out_of_date = True
    glb_current = r.json()['version']

    print(Fore.RED + Style.BRIGHT + 'GLB DB out of date...')
    print(Fore.RED + Style.BRIGHT + 'Downloading...')
    url = r.json()['url']
    r = requests.get(url, allow_redirects=True)
    open(temp_db_name, 'wb').write(r.content)

  # Set second db to download to jp.
  print(Fore.RED + Style.BRIGHT \
        + 'Decrypting Latest Databases... This can take a few minutes...')

  # Calling database decrypt script
  if glb_out_of_date:
    print('Decrypting Global Database')
    decrypt_file(temp_db_name, config.game_env.db_password, str(config.game_env.db_path.absolute()))
    with open('help.txt', 'r') as file:
      data = file.readlines()
      data[0] = str(glb_current) + '\n'
    with open('help.txt', 'w') as file:
      file.writelines(data)

  print(Fore.GREEN + Style.BRIGHT + 'Database update complete.')
