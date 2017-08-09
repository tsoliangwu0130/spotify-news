from flask import Flask, redirect, request
from urllib.parse import quote_plus, urlencode

app = Flask(__name__)
app.config.from_object('config')

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']

CLIENT_SIDE_URL = 'http://localhost'
PORT = 8888
REDIRECT_URI = '{}:{}/callback'.format(CLIENT_SIDE_URL, PORT)

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'


@app.route('/')
def index():
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI
    }
    encoded_auth_url = '{}/?{}'.format(
        SPOTIFY_AUTH_URL,
        urlencode(payload, quote_via=quote_plus)
    )
    return redirect(encoded_auth_url)


@app.route('/callback')
def callback():
    auth_code = request.args['code']
    print('>>>>> auth_code: ', auth_code)
    return 'Hello callback'


if __name__ == '__main__':
    app.run(port=PORT)
