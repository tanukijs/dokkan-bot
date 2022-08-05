import network


def change_name_command():
    # Changes name associated with account
    name = input('What would you like to change your name to?: ')
    r = network.put_user(name=name)
    if 'error' in r:
        print(r)
    else:
        print("Name changed to: " + name)
