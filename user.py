from flask import Blueprint, request, jsonify
from google.cloud import datastore
import constants
import error
import validate
from user_db import *

client = datastore.Client()
bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('', methods=['GET'])
def get_users():
    if not validate.accept_header(request):
        return error.accept_header
    users = get_all_users(request)
    return users, 200