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
import random
import questions
import answers
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

    # key = client.key('EntityKind', 1234)
    # entity = datastore.Entity(key=key)
    # entity.update({
    #     'foo': u'bar',
    #     'baz': 1337,
    #     'qux': False,
    # })
    # client.put(entity)

    #to randomly get a question entity from datastore
    query = client.query(kind='Questions', namespace='Slack_MCQ')
    query.keys_only()
    total = len(list(query.fetch()))
    offset = random.randint(0,total-1)
    selected_qn_id = list(query.fetch(1, offset=offset))[0].id
    key = client.key('Questions', selected_qn_id, namespace='Slack_MCQ')
    entity = client.get(key)
    log.warning(f'entity is: {entity}')

    if (command_text is not None and command_text.lower() == 'quiz'):
        data = questions.populate_question(entity)
    else:
        data = {
            'response_type': 'in_channel',
            'text': 'Please type /hello quiz',
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
    key = client.key('Questions', int(question_id), namespace='Slack_MCQ')
    entity = client.get(key)
    log.warning(f"entity is: {entity}")
    # to extracr the right answer from entity
    qn_answer = None
    i = 0
    while(qn_answer == None):
        if(entity['choices'][i]['right_answer'] == True):
            qn_answer = questions.number_to_alphabet[i]
        i += 1

    if(type is not None and type.lower() == 'interactive_message'):
        if(user_answer is not None and user_answer.lower() == qn_answer.lower()):
            data = answers.populate_right_answer_message(entity, user)
        else:
            data = answers.populate_wrong_answer_message(entity, user)
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
