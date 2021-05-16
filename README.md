[![Coverage Status](https://coveralls.io/repos/github/tykva43/places_remember/badge.svg?branch=master)](https://coveralls.io/github/tykva43/places_remember?branch=master)
[![Tests](https://github.com/tykva43/places_remember/actions/workflows/test.yaml/badge.svg)](https://github.com/tykva43/places_remember/actions/workflows/test.yaml)
# places_remember

It is a web service that allows you to store your impressions of the places you visit.
### Heroku
You can see the project at the following link:
https://places-rmbr.herokuapp.com/


### Installation (Linux)
*Note: You need to customize the example.env file with your settings*
```
$ git clone https://github.com/tykva43/places_remember.git && cd places_remember
$ virtualenv ../venv
$ source ../venv/bin/activate
$ pip install -r requirements.txt
$ cp example.env .env.dev
$ python manage.py migrate
$ python manage.py runserver [<your_ip>:<your_port>] 
```

### Local run with docker
#### Building
```
docker build .
docker-compose build
```
#### Run
```
docker-compose up
```
