# About
Simple Python Flask + SQLite laundry reservation web app. Has no front-end dependencies (no CSS/JS framework, not even jQuery).

# Instructions
## Running the server
Requires Python 3 (e.g. `apt-get install python3`):
```shell
git clone https://github.com/kimsappi/laundry_reservation_flask.git laundry
cd laundry
pip3 install flask sqlalchemy
python3 app.py
```
There is also a Dockerfile available. The port is 8080.

## Accessing the app
Point your browser to http://localhost:8080 or http://0.0.0.0:8080.

# TODO
* SQL injection prevention
* Input validity checking
* UI 
