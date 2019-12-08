from flask import Flask, render_template, request
from sqlalchemy import create_engine
import datetime
import json

import sys

# Configuration
day_count = 4
machines = ['W1', 'W2', 'D1', 'D2']
times = [7, 21]
db_uri = 'sqlite:///reservations.db'
stairs = ['A', 'B', 'C']
apartments = range(1, 19)
delimiter = '@'

app = Flask(__name__)
db = create_engine(db_uri)
dates = [None] * day_count
dates_formatted = [None] * day_count

def day_change():
	for i in range(day_count):
		dates[i] = (datetime.datetime.now() + datetime.timedelta(days=i))
		dates_formatted[i] = (f'{dates[i].day}.{dates[i].month}.')
	day = dates[0].day
	month = dates[0].month
	db.execute(f"""DELETE FROM reservations WHERE month={month} AND day<{day}""")
	if month < 12:
		db.execute(f"""DELETE FROM reservations WHERE month<{month}""")
	if month == 1:
		db.execute(f"""DELETE FROM reservations WHERE month=12""")

@app.route('/')
def index():
	if not dates[0] or dates[0] != datetime.datetime.today():
		day_change()
	day_change()
	reservations = db.execute('SELECT * FROM reservations;')
	reservations_json = '['
	for reservation in reservations:
		if reservations_json != '[':
			reservations_json += ','
		reservations_json += json.dumps(dict(reservation))
	reservations_json += ']'
	return render_template('index.html', dates=dates_formatted, machines=machines, times=range(times[0], times[1] + 1), reservations=reservations_json, stairs=stairs, apartments=apartments, delim=delimiter)

@app.route('/reserve', methods=['POST'])
def reserve():
	data = request.get_json(force=True)
	res_failed = []
	res_success = []
	for reserve in data.get('reserved'):
		r_split = reserve.split(delimiter)
		reservations = db.execute(f'SELECT month FROM reservations WHERE machine="{r_split[0]}" AND day={r_split[1].split(".")[0]} AND month={r_split[1].split(".")[1]} AND hour={r_split[2]};')
		if reservations.first() is not None:
			res_failed.append(reserve)
		else:
			db.execute(f"""INSERT INTO reservations (machine, day, month, hour, cancellation_code, slot_holder) VALUES
				("{r_split[0]}", {r_split[1].split(".")[0]}, {r_split[1].split(".")[1]}, {r_split[2]},
				"{data.get('cancellation_code')}", "{data.get('stair')+data.get('apartment')}");""")
			res_success.append(reserve)
	cancel_failed = []
	cancel_success = []
	for cancel in data.get('cancelled'):
		c_split = cancel.split(delimiter)
		reservations = db.execute(f"""SELECT month FROM reservations
			WHERE machine="{c_split[0]}" AND day={c_split[1].split(".")[0]}\
			AND month={c_split[1].split(".")[1]} AND hour={c_split[2]}
			AND cancellation_code="{data.get('cancellation_code')}";""")
		if reservations.first() is not None:
			db.execute(f"""DELETE FROM reservations
			WHERE machine="{c_split[0]}" AND day={c_split[1].split(".")[0]}\
			AND month={c_split[1].split(".")[1]} AND hour={c_split[2]}
			AND cancellation_code="{data.get('cancellation_code')}";""")
			cancel_success.append(cancel)
		else:
			cancel_failed.append(cancel)
	response = app.response_class(
		status=200,
		mimetype='application/json',
		response=json.dumps({'res_success' : res_success,
			'res_failed' : res_failed,
			'cancel_success' : cancel_success,
			'cancel_failed' : cancel_failed}
		)
	)
	return response

if __name__ == '__main__':
    app.run(debug=True)
