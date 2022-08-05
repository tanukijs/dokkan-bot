import config

from commands.game.complete_stage import complete_stage_command


def complete_area_command(area_id):
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
      print('Completion of area: ' + str(i) + '/' + str(total))
      complete_stage_command(str(quest.id), sugoroku.difficulty)
      i += 1
