import network


def daily_login_command():
    # ## Accepts Outstanding Login Bonuses
    r = network.get_resources_home(
        apologies=True,
        banners=True,
        bonus_schedules=True,
        budokai=True,
        comeback_campaignss=True,
        gifts=True,
        login_bonuses=True,
        rmbattles=True
    )
    if 'error' in r:
        print(r)

    r = network.post_login_bonuses_accept()
    if 'error' in r:
        print(r)
