from flask import Blueprint, request, jsonify
from google.cloud import datastore
import constants
import error
from auth import AuthError, verify_jwt
import validate
from team_db import *
from player_db import view_player_by_id, player_on_team

client = datastore.Client()
bp = Blueprint('team', __name__, url_prefix='/teams')

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    return error.unauthorized

@bp.route('', methods=['POST', 'GET'])
def team_post_view_all():
    payload = verify_jwt(request)
    if isinstance(payload, AuthError):
        return error.unauthorized
    elif not validate.accept_header(request):
        return error.accept_header
    
    if request.method == 'POST':
        # Create a Team
        if not validate.team_request_body(request):
            return error.bad_request
        user_id = get_user_id_by_sub(payload["sub"])
        return create_team(request, user_id)
    if request.method == 'GET':
        # View all Teams
        user_id = get_user_id_by_sub(payload["sub"])
        teams = get_teams_by_user_id(user_id, request)
        return teams, 200

@bp.route('/<team_id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def team_view_put_patch_delete(team_id):
    payload = verify_jwt(request)
    if isinstance(payload, AuthError):
        return error.unauthorized
    elif not validate.accept_header(request):
        return error.accept_header
    team = view_team_by_id(request, team_id)
    user_id = get_user_id_by_sub(payload["sub"])
    if not team:
        return error.team_not_found
    if user_id != team["owner"]:
        return error.forbidden
    
    if request.method == 'GET':
        # View a Team
        return team, 200
    if request.method == 'PATCH':
        # Patch a Team
        patched_team = patch_team_by_id(team_id, request)
        return patched_team, 200
    if request.method == 'PUT':
        # Put a Team
        if not validate.team_request_body(request):
            return error.bad_request
        put_team = put_team_by_id(team_id, request)
        return put_team, 200
    if request.method == 'DELETE':
        # Delete a Team
        delete_team_by_id(team_id)
        return '', 204
    
@bp.route('/<team_id>/players/<player_id>', methods=['PUT', 'DELETE'])
def team_player(team_id, player_id):
    payload = verify_jwt(request)
    if isinstance(payload, AuthError):
        return error.unauthorized
    team = view_team_by_id(request, team_id)
    player = view_player_by_id(request, player_id)
    user_id = get_user_id_by_sub(payload["sub"])
    if not team or not player:
        return error.team_or_player_not_found
    if user_id != team["owner"] or user_id != player["owner"]:
        return error.forbidden
    
    if request.method == 'PUT':
        # Assign Player to Team
        if player_on_team(player_id):
            return error.player_on_team
        assign_player_to_team(team_id, player_id)
        return '', 204