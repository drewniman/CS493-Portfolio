from google.cloud import datastore
import constants
from team_db import get_teams_by_user_id
from player_db import get_players_by_user_id

client = datastore.Client()

def get_all_users(request):
    '''
    Return a list of all users in datastore
    Include id, sub, and number of teams and players owned
    '''
    query = client.query(kind=constants.users)
    results = list(query.fetch())
    for user in results:
        user["id"] = user.key.id
        user["teams"] = get_user_team_count(user.key.id, request)
        user["players"] = get_user_player_count(user.key.id, request)
    return { "users": results, "total": len(results) }

def get_user_team_count(user_id, request):
    '''
    Return the number of teams owned by this user
    '''
    return get_teams_by_user_id(user_id, request)["total"]

def get_user_player_count(user_id, request):
    '''
    Return the number of players owned by this user
    '''
    return get_players_by_user_id(user_id, request)["total"]