#this python files includes all answers related functions
import questions

def populate_question_text(entity, total_choices_num):
    data = entity['question_text'] + '?'
    for i in range(total_choices_num):
        sign = None
        if(entity['choices'][i]['right_answer'] == True):
            sign = ':white_check_mark:'
        else :
            sign = ':x:'
        data = data + '\n' + sign + questions.number_to_alphabet[i] + ': ' + entity['choices'][i]['choice_text']
    return data

def populate_right_answer_message(entity, user):
    data = {
        'response_type': 'in_channel',
        'text': 'Congrats! <@'+ user['id'] +'>, You have got it right',
        'attachments': [
            {
                'text': populate_question_text(entity, len(entity['choices'])),
                'color': '#7FFF00'
            }
        ]
    }
    return data

def populate_wrong_answer_message(entity, user):
    data = {
        'response_type': 'in_channel',
        'text': 'Sorry! <@'+ user['id'] +'>, You have got it wrong',
        'attachments': [
            {
                'text': populate_question_text(entity, len(entity['choices'])),
                'color': '#FF0000'
            }
        ]
    }
    return data
