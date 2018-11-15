# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
from flask import Response
from flask import request
import simplejson as json
import logging
from urllib.parse import parse_qs
#instantiate logger
log = logging.getLogger("my-logger")

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/test',methods = ['POST'])

def test():
    data = {
        'hello'  : 'world',
        'number' : 3,
        'response_type' : 'in_channel',
        'text': 'hello from xy',
        'attachments':
        [
            {
                'text': 'There is no attachments'
            }
        ]
    }

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['content-type'] = 'application/json'
    return resp

def buttonResp():
        json_data = request.get_json()
        user = json_data['user']['name']
        if json_data['actions'][0]['name'] == "A":
            data = {
                'response_type': 'in_channel',
                'text': user +', You are right!',
            }
        else:
            data = {
                'response_type': 'in_channel',
                'text': user +', You are right',
            }

        resp = Response(js,status=200,mimetype='application/json')
        resp.headers['content-type'] = 'application/json'
        return resp;

@app.route('/test',methods = ['POST'])

def test():
    data = {
    "text": "This is a test!!",
    "attachments": [
        {
            "text": "The correct answer is A",
            "fallback": "Choose A please",
            "callback_id": "quiz_test",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "A",
                    "text": "A",
					"style": "danger",
                    "type": "button",
                    "value": "a"
                },
                {
                    "name": "B",
                    "text": "B",
                    "type": "button",
                    "value": "b"
                },
                {
                    "name": "C",
                    "text": "C",                   
                    "type": "button",
                    "value": "c",
                }
            ]
        }
    ]
}
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['content-type'] = 'application/json'

    return resp

@app.route('/hello', methods=['POST'])
def return_quiz():
    #request.get_data()
    #request.form # this is a multdict
    log.warning(request.form)
    command_text = request.form['text']

    if (command_text is not None and command_text.lower() == 'quiz'):
        data = {
            'text': 'Okay, let`s do this mcq qustion.',
            'attachments': [
                {
                    'text': 'What is Alber Einstein`s birthday\nA: 14 March 1879\nB:15 April 1880\nC:16 May 1881\nD:17 June 1882',
                    'fallback': 'You are unable to make the choice',
                    'callback_id': 'einstein_birthday',
                    'color': '#3AA3E3',
                    'attachment_type': 'default',
                    'actions': [
                        {
                            'name': 'birthday',
                            'text': 'A',
                            'type': 'button',
                            'value': 'A',
                            'confirm': {
                                'title': 'Are you sure?',
                                'text': 'Are you sure with this choice?',
                                'ok_text': 'Yes',
                                'dismiss_text': 'No'
                            }
                        },
                        {
                            'name': 'birthday',
                            'text': 'B',
                            'type': 'button',
                            'value': 'B',
                            'confirm': {
                                'title': 'Are you sure?',
                                'text': 'Are you sure with this choice?',
                                'ok_text': 'Yes',
                                'dismiss_text': 'No'
                            }
                        },
                        {
                            'name': 'birthday',
                            'text': 'C',
                            'type': 'button',
                            'value': 'C',
                            'confirm': {
                                'title': 'Are you sure?',
                                'text': 'Are you sure with this choice?',
                                'ok_text': 'Yes',
                                'dismiss_text': 'No'
                            }
                        },
                        {
                            'name': 'birthday',
                            'text': 'D',
                            'type': 'button',
                            'value': 'D',
                            'confirm': {
                                'title': 'Are you sure?',
                                'text': 'Are you sure with this choice?',
                                'ok_text': 'Yes',
                                'dismiss_text': 'No'
                            }
                        }
                        ]
                }
            ]
        }
    else:
        data = {
            'response_type': 'in_channel',
            'text': 'Please type quiz',
            'attachments': [
                {
                    'text': 'This is a reminder message'
                }
            ]
        }

    js = json.dumps(data)
    resp = Response(js,status=200,mimetype='application/json')
    resp.headers['Content-type'] = 'application/json'
    return resp

@app.route('/hello/response', methods=['POST'])
def check_answer():
    log.warning(request.form['payload'])
    #print(request.data)
    json_data = json.loads(request.form['payload'])
    user = json_data['user']['name']
    type = json_data['type']
    answer = json_data['actions'][0]['value']

    if(type is not None and type.lower() == 'interactive_message'):
        if(answer is not None and answer.lower() == 'a'):
            data = {
                'response_type': 'in_channel',
                'text': 'Congrats! '+ user +', You have got it right',
                'attachments': [
                    {
                        'text': 'What is Alber Einstein`s birthday\nA: 14 March 1879\nB:15 April 1880\nC:16 May 1881\nD:17 June 1882',
                        'color': '#7FFF00'
                    }
                ]
            }
        else:
            data = {
                'response_type': 'in_channel',
                'text': 'Sorry! '+ user +', You have got it wrong',
                'attachments': [
                    {
                        'text': 'What is Alber Einstein`s birthday\nA: 14 March 1879\nB:15 April 1880\nC:16 May 1881\nD:17 June 1882',
                        'color': '#FF0000'
                    }
                ]
            }
    else:
        data = {
            'response_type': 'in_channel',
            'text': 'We did not get your message',
            'attachments': [
                {
                    'text': 'This is an error message'
                }
            ]
        }

    js = json.dumps(data)
    resp = Response(js,status=200,mimetype='application/json')
    resp.headers['Content-type'] = 'application/json'
    return resp



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
