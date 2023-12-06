from google.cloud import datastore
import constants

client = datastore.Client()

def create_team(request, user_id):
    '''
    Create a new team in datastore with the given properties
    with owner set to user_id
    '''
    valid_props = ["name", "location", "coach", "mascot", "championships"]
    content = request.get_json()
    team = datastore.Entity(client.key(constants.teams))
    team["owner"] = user_id
    for prop in content:
        if prop in valid_props:
            team[prop] = content[prop]
    client.put(team)
    team["id"] = team.key.id
    team["self"] = request.base_url + '/' + str(team.key.id)
    team["players"] = []
    return team, 201

def get_user_id_by_sub(sub):
    '''
    Return the user_id if user with this sub exists in database
    Otherwise, return False
    '''
    query = client.query(kind=constants.users)
    query.add_filter("sub", "=", sub)
    results = list(query.fetch())
    if len(results) != 1:
        return False
    return results[0].key.id