# This is for users related functions

from google.cloud import datastore
import logging

# instantiate logger
log = logging.getLogger("my-logger")


def user_update_point(client, user, point):
    user_name = user['name']
    user_id = user['id']
    key = client.key('Users', user_id, namespace='Slack_MCQ')
    entity = client.get(key)
    if entity is None:
        entity = datastore.Entity(key=key)
        entity.update({
            'name': user_name,
            'points': point,
        })
    else:
        log.warning(f"entity['points'] is: {entity['points']}")
        entity['points'] += point
    client.put(entity)
    return


# GQL Query error: Your Datastore does not have the composite index (developer-supplied) required for this query.
def populate_leaderboard(client):
    query = client.query(kind='Users', namespace='Slack_MCQ')
    query.order = ['-points']
    query.projection = ['name', 'points']

    text = 'Top 15 players:\nrank   name   points'
    ranking = 1
    medal = ' '
    for entity in query.fetch(limit=15):
        slack_id = ''
        if entity.key.name is not None:
            slack_id = entity.key.name

        if ranking == 1:
            medal = ':first_place_medal:'
        if ranking == 2:
            medal = ':second_place_medal:'
        if ranking == 3:
            medal = ':third_place_medal:'
        text = text + '\n' + medal + 'No.' + str(ranking) + ' <@' + slack_id + '>  ' + str(entity['points'])
        ranking += 1

    data = {
        'response_type': 'ephemeral',
        'text': text,
    }

    return data
