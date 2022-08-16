import webbrowser

from colorama import Fore, Style

import crypto
import network
from classes.Game import GameAccount


class AccountService:
    @staticmethod
    def login(account: GameAccount) -> GameAccount:
        authorization = 'Basic ' + crypto.basic(account.identifier)
        req = network.post_auth_signin(
            authorization=authorization,
            unique_id=account.unique_id
        )

        if 'captcha_url' in req:
            captcha_url = req['captcha_url']
            webbrowser.open(captcha_url, new=2)
            captcha_session_key = req['captcha_session_key']
            print('Opening captcha in browser. Press' + Fore.RED + Style.BRIGHT + ' ENTER ' + Style.RESET_ALL + 'once you have solved it...')
            input()
            req = network.post_auth_signin(
                authorization=authorization,
                unique_id=account.unique_id,
                captcha_session_key=captcha_session_key
            )

        account.access_token = req['access_token']
        account.secret = req['secret']
        return account
