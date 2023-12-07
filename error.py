bad_request = { "Error": "The request object is missing at least one of the required attributes" }, 400
unauthorized = { "Error": "Invalid/missing credentials" }, 401
forbidden = { "Error": "The user is not authorized to access this resource" }, 403
team_not_found = { "Error":  "No team with this team_id exists"} , 404
player_not_found = { "Error":  "No player with this player_id exists"} , 404
accept_header = { "Error": "The Accept header MIME type is not supported by this endpoint" }, 406
team_or_player_not_found = { "Error":  "The specified team and/or player does not exist"} , 404
player_on_team = { "Error":  "The player is already on a team"} , 400