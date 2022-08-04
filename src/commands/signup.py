import base64
import json
import webbrowser

import requests
from colorama import Fore, Style

import config
import crypto
from commands.set_platform import set_platform_command


def signup_command(reroll_state):
    # returns string identifier to be formatted and used by SignIn function

    # Set platform to use
    set_platform_command(reroll_state)

    # Generate AdId and Unique ID to send to Bandai
    config.AdId = crypto.guid()['AdId']
    config.UniqueId = crypto.guid()['UniqueId']

    if config.platform == 'android':
        device_name = 'SM'
        device_model = 'SM-E7000'
        os_version = '7.0'
    else:
        device_name = 'iPhone'
        device_model = 'iPhone XR'
        os_version = '13.0'

    user_acc = {
        'ad_id': config.AdId,
        'country': 'AU',
        'currency': 'AUD',
        'device': device_name,
        'device_model': device_model,
        'os_version': os_version,
        'platform': config.platform,
        'unique_id': config.UniqueId,
    }
    user_account = json.dumps({'user_account': user_acc})

    headers = {
        'User-Agent': config.user_agent,
        'Accept': '*/*',
        'Content-type': 'application/json',
        'X-Platform': config.platform,
        'X-ClientVersion': config.gb_version_code,
    }
    url = config.gb_url + '/auth/sign_up'
    r = requests.post(url, data=user_account, headers=headers)

    # ## It is now necessary to solve the captcha. Opens browser window
    # ## in order to solve it. Script waits for user input before continuing
    print(r.json())
    if 'captcha_url' not in r.json():
        print(Fore.RED + Style.BRIGHT + 'Captcha could not be loaded...')
        return None

    url = r.json()['captcha_url']
    webbrowser.open(url, new=2)
    captcha_session_key = r.json()['captcha_session_key']
    print(
        'Opening captcha in browser. Press' + Fore.RED + Style.BRIGHT + ' ENTER ' + Style.RESET_ALL + 'once you have solved it...')
    input()

    # ## Query sign up again passing the captcha session key.
    # ## Bandais servers check if captcha was solved relative to the session key

    data = {'captcha_session_key': captcha_session_key,
            'user_account': user_acc}

    url = config.gb_url + '/auth/sign_up'

    r = requests.post(url, data=json.dumps(data), headers=headers)

    # ##Return identifier for account, this changes upon transferring account
    try:
        return base64.b64decode(r.json()['identifier']).decode('utf-8')
    except:
        return None
