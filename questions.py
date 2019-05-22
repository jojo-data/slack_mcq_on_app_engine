# this python files includes all questions related functions

import random
import logging

# instantiate logger
log = logging.getLogger("my-logger")

number_to_alphabet = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H'
}


def populate_question_text(entity, total_choices_num):
    data = entity['question_text'] + '?'
    for i in range(total_choices_num):
        data = data + '\n' + number_to_alphabet[i] + ': ' + entity['choices'][i]['choice_text']
    return data


def populate_buttons(id, total_choices_num):
    data = []
    for i in range(total_choices_num):
        item = {
            # name field is mandatory for display any button
            'name': 'birthday',
            'text': number_to_alphabet[i],
            'type': 'button',
            'value': str(id) + ',' + number_to_alphabet[i],
            # REMOVE confirm block to enhance better user experience
            # 'confirm': {
            #     'title': 'Are you sure?',
            #     'text': 'Are you sure with this choice?',
            #     'ok_text': 'Yes',
            #     'dismiss_text': 'No'
            # }
        }
        data.append(item)
    return data


def populate_question(client):
    # to randomly get a question entity from datastore
    query = client.query(kind='Questions', namespace='Slack_MCQ')
    query.keys_only()
    total = len(list(query.fetch()))
    offset = random.randint(0, total - 1)
    selected_qn_id = list(query.fetch(1, offset=offset))[0].id
    key = client.key('Questions', selected_qn_id, namespace='Slack_MCQ')
    entity = client.get(key)
    log.warning(f'entity is: {entity}')

    data = {
        'response_type': 'in_channel',
        'text': 'Okay, let`s do this mcq qustion.',
        'attachments': [
            {
                'text': populate_question_text(entity, len(entity['choices'])),
                'fallback': 'You are unable to make the choice',
                # callback_id is mandatory to trigger a post request to response handling route
                'callback_id': 'alpha_quiz_bot_callback',
                'color': '#3AA3E3',
                'attachment_type': 'default',
                'actions': populate_buttons(entity.id, len(entity['choices']))
            }
        ]
    }
    return data
