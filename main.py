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
from google.cloud import datastore
import questions
import answers
import users
#instantiate logger
log = logging.getLogger("my-logger")

#instantiate datastore client
client = datastore.Client()

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
    #request.get_data()
    #request.form # this is a multdict
    log.warning(f'request.form: {request.form}')
    command_text = request.form['text']

    if (command_text is not None and command_text.lower() == 'quiz'):
        data = questions.populate_question(client)
    elif (command_text is not None and command_text.lower() == 'leaderboard'):
        data = users.populate_leaderboad(client)
    else:
        data = {
            'response_type': 'ephemeral',
            'text': 'Please type /hello quiz for quiz and /hello leaderboard for ranking',
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
    log.warning(f"payload is: {request.form['payload']}")
    #print(request.data)
    json_data = json.loads(request.form['payload'])
    log.warning(f"json_data is: {json_data}")
    user = json_data['user']
    type = json_data['type']
    value = json_data['actions'][0]['value']
    question_id = value.split(',')[0]
    user_answer = value.split(',')[1]

    if(question_id == 'new'):
        if(user_answer == 'yes'):
            data = questions.populate_question(client)
        else:
            resp = Response(status=200)
            return resp
    elif(type is not None and type.lower() == 'interactive_message'):
        key = client.key('Questions', int(question_id), namespace='Slack_MCQ')
        entity = client.get(key)
        log.warning(f"entity is: {entity}")

        qn_answer = answers.extrac_right_answer_from_question_id(entity)

        if(user_answer is not None and user_answer.lower() == qn_answer.lower()):
            data = answers.populate_right_answer_message(entity, user)
            users.user_update_point(client, user, 1)
        else:
            data = answers.populate_wrong_answer_message(entity, user)
            users.user_update_point(client, user, -1)
    else:
        data = {
            'response_type': 'ephemeral',
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
