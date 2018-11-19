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

def populate_question_text_and_next_try_popup(entity, right_answer):
    data = []
    color = None
    if(right_answer):
        color = '#7FFF00'
    else:
        color = '#FF0000'

    question_text = {
        'text': populate_question_text(entity, len(entity['choices'])),
        'color': color
    }
    data.append(question_text)

    next_try_popup = {
        'text': 'Would you like to try another question?',
        'fallback': 'You are unable to make next try',
        #callback_id is mandatory to trigger a post request to response handling route
        'callback_id': 'alpha_quiz_bot_next_try_callback',
        'color': '#3AA3E3',
        'attachment_type': 'default',
        'actions': [
            {
                #name field is mandatory for display any button
                'name': 'next try',
                'text': 'Yes',
                'type': 'button',
                #Value can be anything, the reason to put new, yes here is to coexist with the existing code
                'value': 'new,yes',
            },
            {
                #name field is mandatory for display any button
                'name': 'next try',
                'text': 'No',
                'type': 'button',
                #Value can be anything, the reason to put new, no here is to coexist with the existing code
                'value': 'new,no',
            },
        ]
    }
    data.append(next_try_popup)
    return data


def populate_right_answer_message(entity, user):
    data = {
        'response_type': 'in_channel',
        'text': 'Congrats! <@'+ user['id'] +'>, You have got it right',
        'attachments': populate_question_text_and_next_try_popup(entity, True)
    }
    return data

def populate_wrong_answer_message(entity, user):
    data = {
        'response_type': 'in_channel',
        'text': 'Sorry! <@'+ user['id'] +'>, You have got it wrong',
        'attachments': populate_question_text_and_next_try_popup(entity, False)
    }
    return data

def extrac_right_answer_from_question_id(entity):
    # to extracr the right answer from entity
    qn_answer = None
    i = 0
    while(qn_answer == None):
        if(entity['choices'][i]['right_answer'] == True):
            qn_answer = questions.number_to_alphabet[i]
        i += 1
    return qn_answer
