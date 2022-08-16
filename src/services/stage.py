from typing import Any

from colorama import Style, Fore

import config
import network

_DIFFICULTIES = ['normal', 'very_hard', 'super_hard1', 'super_hard2', 'super_hard3']


class StageService:
    @staticmethod
    def get_friend(stage_id: int, difficulty: int):
        # Returns supporter for given stage_id & difficulty
        # Chooses cpu_supporter if possible
        r = network.get_quests_supporters(
            stage_id=stage_id,
            difficulty=difficulty,
            team_num=1
        )

        # If CPU supporter available, choose it every time
        difficulty_name = _DIFFICULTIES[difficulty]
        if 'cpu_supporters' in r and difficulty_name in r['cpu_supporters']:
            cpu_friends = r['cpu_supporters'][difficulty_name]['cpu_friends']
            if len(cpu_friends) > 0:
                return {
                    'is_cpu': True,
                    'id': cpu_friends[0]['id'],
                    'leader': cpu_friends[0]['card_id']
                }

        return {
            'is_cpu': False,
            'id': r['supporters'][0]['id'],
            'leader': r['supporters'][0]['leader']['card_id']
        }

    @staticmethod
    def get_sign(
        friend,
        kagi,
        difficulty: int,
        selected_team_num: int
    ):
        if not friend['is_cpu']:
            if kagi is not None:
                return {'difficulty': difficulty, 'eventkagi_item_id': kagi, 'friend_id': int(friend['id']),
                        'is_playing_script': True, 'selected_team_num': selected_team_num,
                        'support_leader': {'card_id': int(friend['leader']), 'exp': 0,
                                           'optimal_awakening_step': 0,
                                           'released_rate': 0}}
            else:
                return {'difficulty': difficulty, 'friend_id': int(friend['id']), 'is_playing_script': True,
                        'selected_team_num': selected_team_num,
                        'support_leader': {'card_id': int(friend['leader']), 'exp': 0,
                                           'optimal_awakening_step': 0,
                                           'released_rate': 0}}

        if kagi != None:
            return {'difficulty': difficulty, 'eventkagi_item_id': kagi, 'cpu_friend_id': int(friend['id']),
                    'is_playing_script': True, 'selected_team_num': selected_team_num}

        return {'difficulty': difficulty, 'cpu_friend_id': int(friend['id']), 'is_playing_script': True,
                'selected_team_num': selected_team_num}

    @staticmethod
    def print_rewards(sign: Any):
        if 'items' in sign:
            supportitems = []
            awakeningitems = []
            trainingitems = []
            potentialitems = []
            treasureitems = []
            carditems = []
            trainingfields = []
            stones = 0
            supportitemsset = set()
            awakeningitemsset = set()
            trainingitemsset = set()
            potentialitemsset = set()
            treasureitemsset = set()
            carditemsset = set()
            trainingfieldsset = set()

            if 'quest_clear_rewards' in sign:
                for x in sign['quest_clear_rewards']:
                    if x['item_type'] == 'Point::Stone':
                        stones += x['amount']

            for x in sign['items']:
                if x['item_type'] == 'SupportItem':

                    # print('' + SupportItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                    for i in range(x['quantity']):
                        supportitems.append(x['item_id'])
                    supportitemsset.add(x['item_id'])
                elif x['item_type'] == 'PotentialItem':

                    # print('' + PotentialItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                    for i in range(x['quantity']):
                        potentialitems.append(x['item_id'])
                    potentialitemsset.add(x['item_id'])
                elif x['item_type'] == 'TrainingItem':

                    # print('' + TrainingItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                    for i in range(x['quantity']):
                        trainingitems.append(x['item_id'])
                    trainingitemsset.add(x['item_id'])
                elif x['item_type'] == 'AwakeningItem':

                    # print('' + AwakeningItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                    for i in range(x['quantity']):
                        awakeningitems.append(x['item_id'])
                    awakeningitemsset.add(x['item_id'])
                elif x['item_type'] == 'TreasureItem':

                    # print('' + TreasureItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                    for i in range(x['quantity']):
                        treasureitems.append(x['item_id'])
                    treasureitemsset.add(x['item_id'])
                elif x['item_type'] == 'Card':

                    # card = Cards.find(x['item_id'])

                    carditems.append(x['item_id'])
                    carditemsset.add(x['item_id'])
                elif x['item_type'] == 'Point::Stone':

                    #                print('' + card.name + '['+rarity+']'+ ' x '+str(x['quantity']))
                    # print('' + TreasureItems.find(x['item_id']).name + ' x '+str(x['quantity']))

                    stones += 1
                elif x['item_type'] == 'TrainingField':

                    # card = Cards.find(x['item_id'])

                    for i in range(x['quantity']):
                        trainingfields.append(x['item_id'])
                    trainingfieldsset.add(x['item_id'])
                else:
                    print(x['item_type'])

            for x in supportitemsset:
                config.SupportItems.find_or_fail(x).name
                print(Fore.CYAN + Style.BRIGHT + config.SupportItems.find(x).name + ' x' + str(supportitems.count(x)))

            for x in awakeningitemsset:
                config.AwakeningItems.find_or_fail(x).name
                print(Fore.MAGENTA + Style.BRIGHT + config.AwakeningItems.find(x).name + ' x' + str(
                    awakeningitems.count(x)))

            for x in trainingitemsset:
                config.TrainingItems.find_or_fail(x).name
                print(Fore.RED + Style.BRIGHT + config.TrainingItems.find(x).name + ' x' + str(trainingitems.count(x)))

            for x in potentialitemsset:
                config.PotentialItems.find_or_fail(x).name
                print(config.PotentialItems.find_or_fail(x).name + ' x' + str(potentialitems.count(x)))

            for x in treasureitemsset:
                config.TreasureItems.find_or_fail(x).name
                print(
                    Fore.GREEN + Style.BRIGHT + config.TreasureItems.find(x).name + ' x' + str(treasureitems.count(x)))

            for x in trainingfieldsset:
                config.TrainingFields.find_or_fail(x).name
                print(config.TrainingFields.find(x).name + ' x' + str(trainingfields.count(x)))

            for x in carditemsset:
                config.Cards.find_or_fail(x).name
                print(config.Cards.find(x).name + ' x' + str(carditems.count(x)))

            print(Fore.YELLOW + Style.BRIGHT + 'Stones x' + str(stones))

        zeni = '{:,}'.format(sign['zeni'])
        print('Zeni: ' + zeni)
        if 'gasha_point' in sign:
            print('Friend Points: ' + str(sign['gasha_point']))
