#this python files includes all questions related functions

number_to_alphabet = {
    0 : 'A',
    1 : 'B',
    2 : 'C',
    3 : 'D',
    4 : 'E',
    5 : 'F',
    6 : 'G',
    7 : 'H'
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
            # 'name': 'birthday',
            'text': number_to_alphabet[i],
            'type': 'button',
            'value': str(id) + ',' + number_to_alphabet[i],
            'confirm': {
                'title': 'Are you sure?',
                'text': 'Are you sure with this choice?',
                'ok_text': 'Yes',
                'dismiss_text': 'No'
            }
        }
        data.append(item)
    return data

def populate_question(entity):
    data = {
        'text': 'Okay, let`s do this mcq qustion.',
        'attachments': [
            {
                'text': populate_question_text(entity, len(entity['choices'])),
                'fallback': 'You are unable to make the choice',
                # 'callback_id': 'einstein_birthday',
                'color': '#3AA3E3',
                'attachment_type': 'default',
                'actions': populate_buttons(entity.id, len(entity['choices']))
            }
        ]
    }
    return data
