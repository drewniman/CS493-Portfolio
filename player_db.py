from google.cloud import datastore
import constants

client = datastore.Client()

required_props = ["name", "height", "position", "number"]
optional_props = ["PTS", "REB", "AST", "BLK", "STL", "3PM"]
patchable_props = required_props + optional_props

def create_player(request, user_id):
    '''
    Create a new player in datastore with the given properties
    with owner set to user_id
    '''
    content = request.get_json()
    player = datastore.Entity(client.key(constants.players))
    player["owner"] = user_id
    player["team"] = None
    for prop in required_props:
        player[prop] = content[prop]
    for prop in optional_props:
        if not prop in content:
            player[prop] = None
        else:
            player[prop] = content[prop]
    client.put(player)
    player["id"] = player.key.id
    player["self"] = request.base_url + '/' + str(player.key.id)
    player["players"] = []
    return player, 201

def view_player_by_id(request, player_id):
    '''
    Return the player object, if it exists
    Otherwise, return False
    '''
    player_key = client.key(constants.players, int(player_id))
    player = client.get(key=player_key)
    if not player:
        return False
    player["id"] = player.key.id
    player["self"] = request.base_url
    return player

def get_players_by_user_id(user_id, request):
    '''
    Return a list of players owned by the specified user
    '''
    query = client.query(kind=constants.players)
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
    for player in results:
        player["id"] = player.key.id
    output = { "players": results }
    if next_url:
        output["next"] = next_url
    # Get collection count
    players_count_query = client.aggregation_query(query).count()
    query_result = players_count_query.fetch()
    counts = []
    for aggregation_results in query_result:
        for aggregation in aggregation_results:
            counts.append(aggregation.value)
    output["total"] = counts[0]
    return output

def patch_player_by_id(player_id, request):
    '''
    Update the player props in datastore
    Return updated player on success
    '''
    content = request.get_json()
    player_key = client.key(constants.players, int(player_id))
    player = client.get(key=player_key)
    for prop in content:
        if prop in patchable_props:
            player[prop] = content[prop]
    client.put(player)
    player["id"] = player.key.id
    player["self"] = request.base_url
    return player

def put_player_by_id(player_id, request):
    '''
    Replace all required player props in datastore
    Return updated player on success
    '''
    content = request.get_json()
    player_key = client.key(constants.players, int(player_id))
    player = client.get(key=player_key)
    for prop in required_props:
        player[prop] = content[prop]
    for prop in optional_props:
        if not prop in content:
            player[prop] = None
        else:
            player[prop] = content[prop]
    client.put(player)
    player["id"] = player.key.id
    player["self"] = request.base_url
    return player

def delete_player_by_id(player_id):
    '''
    Delete the specified player from datastore
    '''
    player_key = client.key(constants.players, int(player_id))
    client.delete(player_key)