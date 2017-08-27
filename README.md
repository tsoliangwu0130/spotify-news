# Spotify News [![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

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

## Docker

[Dockerfile](Dockerfile) is also provided. To run this app in a container, just simply install [Docker](https://www.docker.com/) first, then:

1. Build the docker image:

```
$ docker build -t tsoliang/spotify-news .
```

2. Pass the environment variables to Docker container then start the container and expose the container port to local port 5000:

```
$ docker run -d -p 5000:5000 \
             -e CLIENT_ID='<CLIENT_ID>' \
             -e CLIENT_SECRET='<CLIENT_SECRET>' \
             -e REDIRECT_URI='http://localhost:5000/callback' \
             tsoliang/spotify-news
```

##  Screenshot

![screen shot](/images/screenshot.jpg)
