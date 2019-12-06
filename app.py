from flask import Flask, render_template
from sqlalchemy import create_engine
import datetime
import json

# Configuration
day_count = 4
machines = ['W1', 'W2', 'D1', 'D2']
times = [7, 21]
db_uri = 'sqlite:///reservations.db'
stairs = ['A', 'B', 'C']
apartments = range(1, 19)

app = Flask(__name__)
db = create_engine(db_uri)
dates = [None] * day_count
dates_formatted = [None] * day_count

def dates_init():
	for i in range(day_count):
		dates[i] = (datetime.datetime.today() + datetime.timedelta(days=i))
		dates_formatted[i] = (f'{dates[i].day}.{dates[i].month}.')

@app.route('/')
def index():
	if not dates[0] or dates[0] != datetime.datetime.today():
		dates_init()
	reservations = db.execute('SELECT * FROM reservations;')
	reservations_json = '['
	for reservation in reservations:
		if reservations_json != '[':
			reservations_json += ','
		reservations_json += json.dumps(dict(reservation))
	reservations_json += ']'
	return render_template('index.html', dates=dates_formatted, machines=machines, times=range(times[0], times[1] + 1), reservations=reservations_json, stairs=stairs, apartments=apartments)

if __name__ == '__main__':
    app.run(debug=True)
