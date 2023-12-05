from flask import Blueprint, request, jsonify
from google.cloud import datastore
import constants
import error
from auth import AuthError, verify_jwt
import validate

client = datastore.Client()
bp = Blueprint('team', __name__, url_prefix='/teams')

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    return error.credentials_401

@bp.route('', methods=['POST'])
def team_post_get():
    if request.method == 'POST':
        payload = verify_jwt(request)
        if isinstance(payload, AuthError):
            return error.credentials_401
        if not validate.team_request_body(request):
            return error.create_team_400
        elif not validate.accept_header(request):
            return error.create_team_406
        else:
            user_id = get_user_id_by_sub(payload["sub"])
            return create_team(request, user_id)
        

# ================================ DATASTORE FUNCTIONS ================================
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
