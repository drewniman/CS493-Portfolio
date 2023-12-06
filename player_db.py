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

