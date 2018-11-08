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




@app.route('/hello', methods=['POST'])
def return_quiz():
    """Return a simple response"""
    command_text = request.args.get('text')

    if (command_text == 'quiz'):
        data = {
            'text': 'Okay, let`s do this mcq qustion.\nWhat is Alber Einstein`s birthday\nA: 14 March 1879\nB:15 April 1880\nC:16 May 1881\nD:17 June 1882',
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
                        'text': 'Would you prefer another date',
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
                        'text': 'Would you prefer another date',
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
                        'text': 'Would you prefer another date',
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
                        'text': 'Would you prefer another date',
                        'ok_text': 'Yes',
                        'dismiss_text': 'No'
                    }
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
    json_data=request.get_json()
    if(json_data['type'] == 'interactive_message'):
        if(json_data['actions'][0]['value'] == 'a'):
            data = {
                'response_type': 'in_channel',
                'text': 'Congrats! You have got it right',
                'attachments': [
                    {
                        'text': 'This is an correct answer'
                    }
                ]
            }
        else:
            data = {
                'response_type': 'in_channel',
                'text': 'Sorry! You have got it wrong',
                'attachments': [
                    {
                        'text': 'This is an wrong answer'
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
