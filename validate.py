def team_request_body(request):
    content = request.get_json()
    required_props = ["name", "location", "coach", "championships"]
    for prop in required_props:
        if not prop in content:
            return False
    return True

def accept_header(request):
    return 'application/json' in request.accept_mimetypes