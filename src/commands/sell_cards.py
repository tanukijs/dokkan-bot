import network


def sell_cards_command(card_list):
    # Takes cards list and sells them in batches of 99
    cards_to_sell = []
    i = 0
    for card in card_list:
        i += 1
        cards_to_sell.append(card)
        if i == 99:
            r = network.post_cards_sell(cards_to_sell)
            print('Sold Cards x' + str(len(cards_to_sell)))
            if 'error' in r:
                print(r['error'])
                return 0
            i = 0
            cards_to_sell[:] = []
    if i != 0:
        network.post_cards_sell(cards_to_sell)
        print('Sold Cards x' + str(len(cards_to_sell)))
