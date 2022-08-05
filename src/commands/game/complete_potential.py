import config
import network
from commands.game.complete_stage import complete_stage_command


def complete_potential_command():
    events = network.get_events()
    for event in events['events']:
        if event['id'] >= 140 and event['id'] < 145:
            for quest in event['quests']:
                ids = quest['id']
                sugorokus = config.Sugoroku.where('quest_id', '=',
                                                  int(ids)).get()
                difficulties = []
                for sugoroku in sugorokus:
                    complete_stage_command(str(ids), sugoroku.difficulty)
