import json
import webbrowser

import requests
from colorama import Fore, Style

import config
import crypto


def signin_command(identifier):
    # Takes account identifier and encodes it properly, sending BASIC Authorization
    # request to bandai.
    # Returns tuple

    # Format identifier to receive access_token and secret
    basic_accpw = 'Basic ' + crypto.basic(identifier)
    '''
    if ':' in identifier:
        basic_pwacc = identifier.split(':')
        complete_string = basic_pwacc[1] + ':' + basic_pwacc[0]
        basic_accpw = 'Basic ' + base64.b64encode(complete_string.encode('utf-8')).decode('utf-8')
    else:
        basic_accpw = 'Basic ' + base64.b64encode(identifier.encode('utf-8')).decode('utf-8')
    '''

    data = json.dumps({
        'ad_id': crypto.guid()['AdId'],
        'unique_id': crypto.guid()['UniqueId']
    })

    headers = {
        'User-Agent': config.user_agent,
        'Accept': '*/*',
        'Authorization': basic_accpw,
        'Content-type': 'application/json',
        'X-ClientVersion': config.gb_version_code,
        'X-Language': 'en',
        'X-UserCountry': 'AU',
        'X-UserCurrency': 'AUD',
        'X-Platform': config.platform,
    }
    url = config.gb_url + '/auth/sign_in'

    r = requests.post(url, data=data, headers=headers)

    if 'captcha_url' in r.json():
        cap_url = r.json()['captcha_url']
        webbrowser.open(cap_url, new=2)
        captcha_session_key = r.json()['captcha_session_key']
        print(
            'Opening captcha in browser. Press' + Fore.RED + Style.BRIGHT + ' ENTER ' + Style.RESET_ALL + 'once you have solved it...')
        input()
        data = json.dumps({
            'captcha_session_key': captcha_session_key,
            'ad_id': crypto.guid()['AdId'],
            'unique_id': crypto.guid()['UniqueId'],
        })
        r = requests.post(url, data=data, headers=headers)

    print(Fore.RED + Style.BRIGHT + 'SIGN IN COMPLETE' + Style.RESET_ALL)

    try:
        return (r.json()['access_token'], r.json()['secret'])
    except:
        return None
