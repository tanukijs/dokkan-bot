import config

from commands import stage

NAME = 'area'
DESCRIPTION = 'Completes the given area'
CONTEXT = [config.GameContext.GAME]


def run(area_id: int):
    quests = config.Quests.where('area_id', '=', area_id).get()
    total = 0

    for quest in quests:
        sugorokus = config.Sugoroku.where('quest_id', '=', quest.id).get()
        total += len(sugorokus)

    i = 1
    for quest in quests:
        sugorokus = config.Sugoroku.where('quest_id', '=', quest.id).get()
        difficulties = []
        for sugoroku in sugorokus:
            print('Completion of area:', str(i) + '/' + str(total), '(' + str(round((i / total) * 100)) + '%)')
            stage.run(quest.id, sugoroku.difficulty)
            i += 1
