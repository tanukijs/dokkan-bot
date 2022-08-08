import config
import network

NAME = 'info'
DESCRIPTION = 'Account summary'


def run():
    user = network.get_user()
    print('Name: ' + str(user['user']['name']))
    print('Account ID: ' + str(user['user']['id']))
    print('Platform: ' + config.game_platform.name)
    print('Stones: ' + str(user['user']['stone']))
    print('Zeni: ' + str(user['user']['zeni']))
    print('Rank: ' + str(user['user']['rank']))
    print('ACT: ' + str(user['user']['act']))
    print('Card capacity: ' + str(user['user']['total_card_capacity']))
