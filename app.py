from flask import Flask, render_template, request
from sqlalchemy import create_engine
from validate_passcode import validate_passcode
import datetime
import json
import os

# Configuration
day_count = 5
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
	try:
		db.execute(f"""DELETE FROM reservations WHERE month={month} AND day<{day};""")
		if month < 12:
			db.execute(f"""DELETE FROM reservations WHERE month<{month};""")
		if month == 1:
			db.execute(f"""DELETE FROM reservations WHERE month=12;""")
	except:
		db.execute("""CREATE TABLE machines (id VARCHAR(20) NOT NULL);""")
		db.execute("""CREATE TABLE reservations (
			day INTEGER NOT NULL,
			month INTEGER NOT NULL,
			hour INTEGER NOT NULL,
			cancellation_code VARCHAR(50),
			machine VARCHAR(20) NOT NULL,
			slot_holder VARCHAR(20) NOT NULL,
			FOREIGN KEY (machine) REFERENCES machines(id),
			PRIMARY KEY (machine,day,month,hour));""")
		for machine in machines:
			db.execute(f"""INSERT INTO machines VALUES('{machine}');""")

@app.route('/')
def index():
	if not dates[0] or dates[0] != datetime.datetime.today():
		day_change()
	reservations = db.execute('SELECT * FROM reservations;')
	reservations_json = '['
	for reservation in reservations:
		if reservations_json != '[':
			reservations_json += ','
		res_dict = dict(reservation)
		del res_dict['cancellation_code']
		reservations_json += json.dumps(res_dict)
	reservations_json += ']'
	return render_template('index_en.html', dates=dates_formatted, machines=machines, times=range(times[0], times[1] + 1), reservations=reservations_json, stairs=stairs, apartments=apartments, delim=delimiter)

@app.route('/reserve', methods=['POST'])
def reserve():
	data = request.get_json(force=True)
	res_failed = []
	res_success = []
	for reserve in data.get('reserved'):
		r_split = reserve.split(delimiter)
		reservations = db.execute(f'SELECT month FROM reservations WHERE machine="{r_split[0]}" AND day={r_split[1].split(".")[0]} AND month={r_split[1].split(".")[1]} AND hour={r_split[2]};')
		if reservations.first() is not None or validate_passcode(data) == False:
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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
