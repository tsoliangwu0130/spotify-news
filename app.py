import json
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template, request, url_for
from urllib.parse import quote_plus, urlencode

app = Flask(__name__)
app.config.from_object('config')

CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
SCOPE = 'user-read-currently-playing user-read-playback-state'
TOKEN_HEADER = {}

CLIENT_SIDE_URL = 'http://localhost'
PORT = 8888
REDIRECT_URI = '{}:{}/callback'.format(CLIENT_SIDE_URL, PORT)

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'
SPOTIFY_API_USER_PROFILE_ENDPOINT = SPOTIFY_API_BASE_URL + '/me'
SPOTIFY_API_CURRENT_PLAYBACK_ENDPOINT = SPOTIFY_API_USER_PROFILE_ENDPOINT + '/player'

GOOGLE_SEARCH_URL = 'https://www.google.com/search'


def fetch_news(q):
    fetched_news = []

    search_payload = {
        'q': q,
        'tbm': 'nws'
    }
    res_html = requests.get(url=GOOGLE_SEARCH_URL, params=search_payload)
    soup = BeautifulSoup(res_html.text, 'html.parser')
    news = soup.find('div', {'id': 'ires'}).find_all('div', {'class': 'g'})

    for item in news:
        title = item.find('h3').text
        url = re.findall(r'(http.+?)&', item.find('a')['href'])[0]
        prev_content = item.find('div', {'class': 'st'}).text
        fetched_news.append({'title': title, 'url': url, 'prev_content': prev_content})
    return fetched_news


@app.route('/')
def index():
    if not TOKEN_HEADER:
        return redirect(url_for('login'))

    profile_res = requests.get(SPOTIFY_API_USER_PROFILE_ENDPOINT, headers=TOKEN_HEADER)
    cur_playback_res = requests.get(SPOTIFY_API_CURRENT_PLAYBACK_ENDPOINT, headers=TOKEN_HEADER)

    profile_data = json.loads(profile_res.text)
    cur_playback_data = json.loads(cur_playback_res.text)

    artists = cur_playback_data['item']['artists']
    # TODO: fetch all artists' news
    artist = artists[0]['name']

    fetched_news = fetch_news(artist)
    return render_template(
        'index.html',
        profile=profile_data,
        cur_playback=cur_playback_data,
        fetched_news=fetched_news
    )


@app.route('/login')
def login():
    auth_payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    encoded_auth_url = '{}/?{}'.format(
        SPOTIFY_AUTH_URL,
        urlencode(auth_payload, quote_via=quote_plus)
    )
    return redirect(encoded_auth_url)


@app.route('/callback')
def callback():
    global TOKEN_HEADER

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
    token_data = json.loads(token_result.text)
    TOKEN_HEADER = {'Authorization': '{} {}'.format(token_data['token_type'], token_data['access_token'])}

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=PORT)
