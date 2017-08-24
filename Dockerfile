FROM python:3.6

# Create app directory
RUN mkdir -p /usr/src/spotify-news
WORKDIR /usr/src/spotify-news

# Install app dependencies
COPY requirements.txt /usr/src/spotify-news/
RUN pip install -r requirements.txt

# Bundle app source
COPY . /usr/src/spotify-news

EXPOSE 5000
USER nobody:nogroup
CMD [ "python", "app.py" ]
