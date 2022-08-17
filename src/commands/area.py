import config

import models.game
from commands import stage

NAME = 'area'
DESCRIPTION = 'Completes the given area'
CONTEXT = [config.GameContext.GAME]


def run(area_id: int):
    quests: list[models.game.Quests] = models.game.Quests.select().where(models.game.Quests.area_id == area_id)
    total = 0

    for quest in quests:
        sugorokus: list[models.game.SugorokuMaps] = models.game.SugorokuMaps.select().where(models.game.SugorokuMaps.quest_id == quest.id)
        total += len(sugorokus)

    i = 1
    for quest in quests:
        sugorokus: list[models.game.SugorokuMaps] = models.game.SugorokuMaps.select().where(models.game.SugorokuMaps.quest_id == quest.id)
        difficulties = []
        for sugoroku in sugorokus:
            print('Completion of area:', str(i) + '/' + str(total), '(' + str(round((i / total) * 100)) + '%)')
            stage.run(quest.id, sugoroku.difficulty)
            i += 1
