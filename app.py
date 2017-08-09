from flask import Flask, redirect, request
from urllib.parse import quote_plus, urlencode

import json
import requests

app = Flask(__name__)
app.config.from_object('config')

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']

CLIENT_SIDE_URL = 'http://localhost'
PORT = 8888
REDIRECT_URI = '{}:{}/callback'.format(CLIENT_SIDE_URL, PORT)

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'


@app.route('/')
def index():
    auth_payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI
    }
    encoded_auth_url = '{}/?{}'.format(
        SPOTIFY_AUTH_URL,
        urlencode(auth_payload, quote_via=quote_plus)
    )
    return redirect(encoded_auth_url)


@app.route('/callback')
def callback():
    token_payload = {
        'grant_type': 'authorization_code',
        'code': request.args['code'],
        'redirect_uri': REDIRECT_URI
    }
    token_result = requests.post(
        SPOTIFY_TOKEN_URL,
        data=token_payload,
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    token_json = json.loads(token_result.text)
    token_header = {'Authorization': '{} {}'.format(token_json['token_type'], token_json['access_token'])}

    user_profile_api_endpoint = 'https://api.spotify.com/v1/me'
    profile_response = requests.get(user_profile_api_endpoint, headers=token_header)
    profile_data = json.loads(profile_response.text)

    return json.dumps(profile_data, indent=4, sort_keys=True)


if __name__ == '__main__':
    app.run(port=PORT)
