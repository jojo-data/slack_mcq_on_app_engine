#This is for users related functions

from google.cloud import datastore

def user_update_point(client, user, point):
    user_name = user['name']
    user_id = user['id']
    key = client.key('Users', user_id, namespace='Slack_MCQ')
    entity = client.get(key)
    if(entity == None):
        entity = datastore.Entity(key=key)
        entity.update({
            'name': user_name,
            'points': point,
        })
    else:
        print(f"entity['points'] is: {entity['points']}")
        entity['points'] += point
    client.put(entity)
    return
