import config
import network
from commands import stage

NAME = 'potential'
DESCRIPTION = 'Completes potential stages'
CONTEXT = [config.GameContext.GAME]


def run():
    events = network.get_events()
    for event in events['events']:
        if 140 <= event['id'] < 145:
            for quest in event['quests']:
                quest_id = int(quest['id'])
                sugorokus = config.Sugoroku.where('quest_id', '=', quest_id).get()
                difficulties = []
                for sugoroku in sugorokus:
                    stage.run(quest_id, sugoroku.difficulty)
