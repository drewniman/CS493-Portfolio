from flask import Blueprint, request, jsonify
from google.cloud import datastore
import constants
import error
from auth import AuthError, verify_jwt
import validate
from team_db import *

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
        else:
            user_id = get_user_id_by_sub(payload["sub"])
            return create_team(request, user_id)
    if request.method == 'GET':
        # View all Teams
        user_id = get_user_id_by_sub(payload["sub"])
        teams = get_teams_by_user_id(user_id, request)
        return teams, 200

@bp.route('/<team_id>', methods=['GET'])
def team_view_put_patch_delete(team_id):
    if request.method == 'GET':
        # View a Team
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
        return team, 200
