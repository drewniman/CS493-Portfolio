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
