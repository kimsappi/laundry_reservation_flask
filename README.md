# About
Simple Python Flask + SQLite laundry reservation web app. Has no front-end dependencies (no CSS/JS frameworks/libraries).

There is a demo available on [Heroku](http://kimsappi-laundry-demo.herokuapp.com/). All data is reset after 30 minutes of inactivity on the demo.

# Instructions
## Running the server
Requires Python 3 (e.g. `apt-get install python3`):
```shell
git clone https://github.com/kimsappi/laundry_reservation_flask.git laundry
cd laundry
pip3 install flask sqlalchemy
python3 app.py
```
There is also a Dockerfile available.

## Accessing the app
Point your browser to http://localhost:5000 or http://0.0.0.0:5000.

# TODO
* SQL injection prevention
* Input validity checking
* UI
