import network


def get_remaining_stones_command():
    user = network.get_user()
    return 'Stones: ' + str(user['user']['stone'])
