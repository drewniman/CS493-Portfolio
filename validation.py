def valid_team_request_body(request):
    content = request.get_json()
    required_props = ["name", "location", "coach", "mascot", "championships"]
    for prop in required_props:
        if not prop in content:
            return False
    return True

def valid_accept_header(request):
    return 'application/json' in request.accept_mimetypes