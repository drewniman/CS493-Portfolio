def team_request_body(request):
    content = request.get_json()
    required_props = ["name", "location", "coach", "championships"]
    optional_props = ["mascot"]
    for prop in required_props:
        if not prop in content:
            return False
    for prop in content:
        if not (prop in required_props + optional_props):
            return False
    return True

def accept_header(request):
    return 'application/json' in request.accept_mimetypes

def player_request_body(request):
    content = request.get_json()
    required_props = ["name", "height", "position", "number"]
    optional_props = ["PTS", "REB", "AST", "BLK", "STL", "3PM"]
    for prop in required_props:
        if not prop in content:
            return False
    for prop in content:
        if not (prop in required_props + optional_props):
            return False
    return True