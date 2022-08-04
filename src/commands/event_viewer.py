import PySimpleGUI as sg
import requests

import config
from commands.complete_stage import complete_stage_command
from network.utils import generate_headers


def event_viewer_command():
    # Event GUI with options to complete stage.
    # JP Translation needs work

    headers = generate_headers('GET', '/events')
    url = config.gb_url + '/events'
    r = requests.get(url, headers=headers)
    events = r.json()

    # Build areas list
    areas_to_display = []
    stage_ids = []
    areas = {}

    for event in events['events']:
        area_id = str(event['id'])
        try:
            config.Model.set_connection_resolver(config.db_glb)
            area_name = area_id + ' | ' + str(config.Area.where('id', '=', area_id).first().name)
        except:
            config.Model.set_connection_resolver(config.db_jp)
            area_name = area_id + ' | ' + str(config.Area.where('id', '=', area_id).first().name)
        areas_to_display.append(area_name)
        stage_ids[:] = []
        for quest in event['quests']:
            stage_ids.append(quest['id'])
        areas[area_id] = stage_ids[:]

    stages_to_display = []
    difficulties = [0]
    stage_name = ''

    col1 = [[sg.Listbox(values=(sorted(areas_to_display)), change_submits=True, size=(30, 20), key='AREAS')]]
    col2 = [[sg.Listbox(values=(sorted(stages_to_display)), change_submits=True, size=(30, 20), key='STAGES')]]
    col3 = [[sg.Text('Name', key='STAGE_NAME', size=(30, 2))],
            [sg.Text('Difficulty: '), sg.Combo(difficulties, key='DIFFICULTIES', size=(6, 3), readonly=True)],
            [sg.Text('How many times to complete:')
                , sg.Spin([i for i in range(1, 999)], key='LOOP', initial_value=1, size=(3, 3))],
            [sg.Button(button_text='Complete Stage', key='COMPLETE_STAGE')]]

    layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3)]]
    window = sg.Window('Event Viewer').Layout(layout)

    while True:
        event, values = window.Read()
        if event == None:
            return 0

        if event == 'AREAS' and len(values['AREAS']) > 0:
            stages_to_display[:] = []
            # Check if GLB database has id, if not try JP DB.   
            area_id = values['AREAS'][0].split(' | ')[0]

            for stage_id in areas[area_id]:
                try:
                    config.Model.set_connection_resolver(config.db_glb)
                    stage_name = config.Quests.find_or_fail(stage_id).name
                except:
                    config.Model.set_connection_resolver(config.db_jp)
                    stage_name = config.Quests.find_or_fail(stage_id).name
                stages_to_display.append(stage_name + ' | ' + str(stage_id))

        if event == 'STAGES' and len(values['STAGES']) > 0:
            difficulties[:] = []
            stage_id = values['STAGES'][0].split(' | ')[1]
            stage_name = values['STAGES'][0].split(' | ')[0]
            sugorokus = config.Sugoroku.where('quest_id', '=', str(stage_id)).get()
            difficulties = []
            for sugoroku in sugorokus:
                difficulties.append(str(sugoroku.difficulty))
            window.FindElement('DIFFICULTIES').Update(values=difficulties)
            window.FindElement('STAGE_NAME').Update(stage_name)

        if event == 'COMPLETE_STAGE' and stage_name != '':
            window.Hide()
            window.Refresh()
            for i in range(int(values['LOOP'])):
                complete_stage_command(stage_id, values['DIFFICULTIES'])
            window.UnHide()
            window.Refresh()

        window.FindElement('STAGES').Update(values=stages_to_display)
