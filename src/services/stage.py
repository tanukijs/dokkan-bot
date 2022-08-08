import network


class StageService:
    @staticmethod
    def get_friend(stage_id, difficulty):
        # Returns supporter for given stage_id & difficulty
        # Chooses cpu_supporter if possible
        r = network.get_quests_supporters(
            stage_id=stage_id,
            difficulty=difficulty,
            team_num=1
        )

        # If CPU supporter available, choose it every time
        if 'cpu_supporters' in r:
            if int(difficulty) == 5:
                if 'super_hard3' in r['cpu_supporters']:
                    if len(r['cpu_supporters']['super_hard3'
                           ]['cpu_friends']) > 0:
                        return {
                            'is_cpu': True,
                            'id': r['cpu_supporters']['super_hard3']
                            ['cpu_friends'][0]['id'],
                            'leader': r['cpu_supporters']['super_hard3']
                            ['cpu_friends'][0]['card_id']
                        }
            if int(difficulty) == 4:
                if 'super_hard2' in r['cpu_supporters']:
                    if len(r['cpu_supporters']['super_hard2'
                           ]['cpu_friends']) > 0:
                        return {
                            'is_cpu': True,
                            'id': r['cpu_supporters']['super_hard2']
                            ['cpu_friends'][0]['id'],
                            'leader': r['cpu_supporters']['super_hard2']
                            ['cpu_friends'][0]['card_id']
                        }
            if int(difficulty) == 3:
                if 'super_hard1' in r['cpu_supporters']:
                    if len(r['cpu_supporters']['super_hard1'
                           ]['cpu_friends']) > 0:
                        return {
                            'is_cpu': True,
                            'id': r['cpu_supporters']['super_hard1']
                            ['cpu_friends'][0]['id'],
                            'leader': r['cpu_supporters']['super_hard1']
                            ['cpu_friends'][0]['card_id']
                        }
            if int(difficulty) == 2:
                if 'very_hard' in r['cpu_supporters']:
                    if len(r['cpu_supporters']['very_hard'
                           ]['cpu_friends']) > 0:
                        return {
                            'is_cpu': True,
                            'id': r['cpu_supporters']['very_hard']
                            ['cpu_friends'][0]['id'],
                            'leader': r['cpu_supporters']['very_hard']
                            ['cpu_friends'][0]['card_id']
                        }
            if int(difficulty) == 1:
                if 'hard' in r['cpu_supporters']:
                    if len(r['cpu_supporters']['hard']['cpu_friends'
                           ]) > 0:
                        return {
                            'is_cpu': True,
                            'id': r['cpu_supporters']['hard']
                            ['cpu_friends'][0]['id'],
                            'leader': r['cpu_supporters']['hard']
                            ['cpu_friends'][0]['card_id']
                        }
            if int(difficulty) == 0:
                if 'normal' in r['cpu_supporters']:
                    if len(r['cpu_supporters']['normal'
                           ]['cpu_friends']) > 0:
                        return {
                            'is_cpu': True,
                            'id': r['cpu_supporters']['normal']
                            ['cpu_friends'][0]['id'],
                            'leader': r['cpu_supporters']['normal']
                            ['cpu_friends'][0]['card_id']
                        }

        return {
            'is_cpu': False,
            'id': r['supporters'][0]['id'],
            'leader': r['supporters'][0]['leader']['card_id']
        }
