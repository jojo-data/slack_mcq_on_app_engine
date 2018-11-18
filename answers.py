#this python files includes all answers related functions

import questions

def populate_right_answer_message(entity, user):
    data = {
        'response_type': 'in_channel',
        'text': 'Congrats! '+ user +', You have got it right',
        'attachments': [
            {
                'text': questions.populate_question_text(entity, len(entity['choices'])),
                'color': '#7FFF00'
            }
        ]
    }
    return data

def populate_wrong_answer_message(entity, user):
    data = {
        'response_type': 'in_channel',
        'text': 'Sorry! '+ user +', You have got it wrong',
        'attachments': [
            {
                'text': questions.populate_question_text(entity, len(entity['choices'])),
                'color': '#FF0000'
            }
        ]
    }
    return data
