import config
import network


def get_user_info_command():
    user = network.get_user()

    print('Account OS: ' + config.game_platform.name)
    print('User ID: ' + str(user['user']['id']))
    print('Stones: ' + str(user['user']['stone']))
    print('Zeni: ' + str(user['user']['zeni']))
    print('Rank: ' + str(user['user']['rank']))
    print('Stamina: ' + str(user['user']['act']))
    print('Name: ' + str(user['user']['name']))
    print('Total Card Capacity: ' + str(user['user']['total_card_capacity']))
