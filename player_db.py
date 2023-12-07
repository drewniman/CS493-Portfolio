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