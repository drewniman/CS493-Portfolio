from flask import Blueprint, request, jsonify
from google.cloud import datastore
import constants
import error
from auth import AuthError, verify_jwt
import validate
from player_db import *
from team_db import get_user_id_by_sub

client = datastore.Client()
bp = Blueprint('player', __name__, url_prefix='/players')

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    return error.unauthorized

@bp.route('', methods=['POST'])
def player_post_view_all():
    payload = verify_jwt(request)
    if isinstance(payload, AuthError):
        return error.unauthorized
    elif not validate.accept_header(request):
        return error.accept_header
    
    if request.method == 'POST':
        # Create a Player
        if not validate.player_request_body(request):
            return error.bad_request
        user_id = get_user_id_by_sub(payload["sub"])
        return create_player(request, user_id)
    # if request.method == 'GET':
    #     # View all Teams
    #     user_id = get_user_id_by_sub(payload["sub"])
    #     teams = get_teams_by_user_id(user_id, request)
    #     return teams, 200