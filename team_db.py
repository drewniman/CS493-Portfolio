from google.cloud import datastore
import constants

client = datastore.Client()

required_props = ["name", "location", "coach", "championships"]
optional_props = ["mascot"]

def create_team(request, user_id):
    '''
    Create a new team in datastore with the given properties
    with owner set to user_id
    '''
    content = request.get_json()
    team = datastore.Entity(client.key(constants.teams))
    team["owner"] = user_id
    for prop in required_props:
        team[prop] = content[prop]
    for prop in optional_props:
        if not prop in content:
            team[prop] = None
        else:
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

def view_team_by_id(request, team_id):
    '''
    Return the team object, if it exists
    Otherwise, return False
    '''
    team_key = client.key(constants.teams, int(team_id))
    team = client.get(key=team_key)
    if not team:
        return False
    # for prop in optional_props:
    #     if prop not in team:
    #         team[prop] = None
    team["id"] = team.key.id
    team["self"] = request.base_url
    team["players"] = get_players_on_team(team_id)
    return team

def get_players_on_team(team_id):
    '''
    TODO
    Return a list of players on the team's roster
    '''
    return []