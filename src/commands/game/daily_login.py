import network


def daily_login_command():
    network.get_resources_home(
        apologies=True,
        banners=True,
        bonus_schedules=True,
        budokai=True,
        dragonball_sets=True,
        gifts=True,
        login_bonuses=True,
        missions=True,
        random_login_bonuses=True,
        rmbattles=True,
        comeback_campaigns=True
    )

    network.post_login_bonuses_accept()
