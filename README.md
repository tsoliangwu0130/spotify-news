# Spotify News

A [Flask](http://flask.pocoo.org/) app (Python 3) to retrieve the singers' latest news according to your [Spotify](https://www.spotify.com/) current playing song.

## Configuration

Register a application with [Spotify Developer](https://developer.spotify.com/), then export `Client ID`, `Client Secret` and `Redirect URIs` as environment variables:

```
$ export CLIENT_ID='<CLIENT_ID>'
$ export CLIENT_SECRET='<CLIENT_SECRET>'
$ export REDIRECT_URI='http://localhost:5000/callback'
```

## Usage

1. To install app dependencies, simply run:

```
$ pip install -r requirements.txt
```

2. Start the app at [localhost:5000](http://localhost:5000):

```
$ python app.py
```

##  Screenshot

![screen shot](/images/screenshot.jpg)
