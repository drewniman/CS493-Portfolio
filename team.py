from flask import Blueprint, request
from google.cloud import datastore
import constants

client = datastore.Client()
bp = Blueprint('team', __name__, url_prefix='/teams')

@bp.route('', methods=['POST'])
def team_post_get():
    if request.method == 'POST':
        if not valid_create_team_request(request):
            return constants.invalid_create_team_request
        elif not valid_accept_header(request):
            return constants.invalid_accept_header
        else:
            return create_team(request)
        

# ================================ DATASTORE FUNCTIONS ================================
def create_team(request):
    content = request.get_json()
    team = datastore.Entity(client.key(constants.teams))
    team.update(
        {
            "name": content["name"],
            "location": content["location"],
            "coach": content["coach"],
            "mascot": content["mascot"],
            "championships": content["championships"],
            "coach": content["coach"],
            "coach": content["coach"],
        }
    )
    client.put(team)
    team["id"] = team.key.id
    team["self"] = request.base_url + '/' + str(team.key.id)
    return team, 201

# ================================ VALIDATION FUNCTIONS ================================
def valid_create_team_request(request):
    content = request.get_json()
    required_props = ["name", "location", "coach", "mascot", "championships"]
    for prop in required_props:
        if not prop in content:
            return False
    return True

def valid_accept_header(request):
    return 'application/json' in request.accept_mimetypes