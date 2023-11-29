from flask import Flask
import team

app = Flask(__name__)
app.register_blueprint(team.bp)

@app.route('/')
def index():
    return "Please navigate to /teams, /players, or /users to use this API"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
