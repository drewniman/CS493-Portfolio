from google.cloud import datastore
import constants

client = datastore.Client()

required_props = ["name", "location", "coach", "championships"]
optional_props = ["mascot"]
patchable_props = required_props + optional_props

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
    team["id"] = team.key.id
    team["self"] = request.base_url
    team["players"] = get_players_on_team(team_id, request)
    return team

def get_players_on_team(team_id, request):
    '''
    TODO
    Return a list of players on the team's roster
    Only includes id and self link
    '''
    return []

def get_teams_by_user_id(user_id, request):
    '''
    Return a list of teams owned by the specified user
    '''
    query = client.query(kind=constants.teams)
    query.add_filter("owner", "=", int(user_id))
    q_limit = int(request.args.get('limit', '5'))
    q_offset = int(request.args.get('offset', '0'))
    l_iterator = query.fetch(limit= q_limit, offset=q_offset)
    pages = l_iterator.pages
    results = list(next(pages))
    next_url = None
    if l_iterator.next_page_token:
        next_offset = q_offset + q_limit
        next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
    for team in results:
        team["id"] = team.key.id
        team["players"] = get_players_on_team(team.key.id, request)
    output = { "teams": results }
    if next_url:
        output["next"] = next_url
    # Get collection count
    teams_count_query = client.aggregation_query(query).count()
    query_result = teams_count_query.fetch()
    counts = []
    for aggregation_results in query_result:
        for aggregation in aggregation_results:
            counts.append(aggregation.value)
    output["total"] = counts[0]
    return output

def patch_team_by_id(team_id, request):
    '''
    Update the team props in datastore
    Return updated team on success
    '''
    content = request.get_json()
    team_key = client.key(constants.teams, int(team_id))
    team = client.get(key=team_key)
    for prop in content:
        if prop in patchable_props:
            team[prop] = content[prop]
    client.put(team)
    team["id"] = team.key.id
    team["players"] = get_players_on_team(team, request)
    team["self"] = request.base_url
    return team

def put_team_by_id(team_id, request):
    '''
    Replace all required team props in datastore
    Return updated team on success
    '''
    content = request.get_json()
    team_key = client.key(constants.teams, int(team_id))
    team = client.get(key=team_key)
    for prop in required_props:
        team[prop] = content[prop]
    for prop in optional_props:
        if not prop in content:
            team[prop] = None
        else:
            team[prop] = content[prop]
    client.put(team)
    team["id"] = team.key.id
    team["players"] = get_players_on_team(team, request)
    team["self"] = request.base_url
    return team