import config
import models.game
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
                sugorokus: list[models.game.SugorokuMaps] = models.game.SugorokuMaps.select().where(models.game.SugorokuMaps.quest_id == quest_id).get()
                difficulties = []
                for sugoroku in sugorokus:
                    stage.run(quest_id, sugoroku.difficulty)
