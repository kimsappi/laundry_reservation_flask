function add_slot_holder(parent, slot_holder) {
	let div = document.createElement('div');
	div.classList.add('slot_holder');
	div.innerText = slot_holder;
	parent.appendChild(div);
}

function validate_inputs()
{
	let submission_error = ''
	let stair = document.getElementById('stair');
	stair = stair.options[stair.selectedIndex].value;
	if (stair === '' && user_res.length > 0) {
		submission_error += 'You must select a stair.\n'
	}
	let apartment = document.getElementById('apartment');
	apartment = apartment.options[apartment.selectedIndex].value;
	if (apartment === '' && user_res.length > 0) {
		submission_error += 'You must select an apartment.\n';
	}
	let passcode = document.getElementById('passcode').value;
	if (passcode === '' && user_res.length > 0) {
		submission_error += 'You must select a passcode.\n';
	}
	let cancellation_code = document.getElementById('cancellation_code').value;
	if (cancellation_code === '') {
		submission_error += 'You must select a cancellation code.\n';
	}
	if (user_res.length === 0 && user_cancel.length === 0) {
		submission_error += 'You must reserve or cancel a slot.';
	}

	if (submission_error === '') {
		return {"stair" : stair, "apartment" : apartment, "passcode" : passcode, "cancellation_code" : cancellation_code, "reserved" : user_res, "cancelled" : user_cancel};
	}
	else {
		alert(submission_error);
		return null;
	}
}

function submission_results(response) {
	for (let slot of response.res_success) {
		let index = user_res.indexOf(slot);
		if (index > -1) {
			user_res.splice(index, 1);
		}
		document.getElementById(slot).classList.replace('reserving', 'newly_reserved');
		let stair = document.getElementById('stair');
		stair = stair.options[stair.selectedIndex].value;
		let apartment = document.getElementById('apartment');
		apartment = apartment.options[apartment.selectedIndex].value;
		add_slot_holder(document.getElementById(slot), stair+apartment);
	}
	for (let slot of response.cancel_success) {
		document.getElementById(slot).classList.replace('dereserving', 'free');
		let index = user_cancel.indexOf(slot);
		if (index > -1) {
			user_res.splice(index, 1);
		}
	}
	let res_failure = 'Reservation failure:\n';
	for (let slot of response.res_failed) {
		document.getElementById(slot).classList.replace('reserving', 'free');
		let index = user_res.indexOf(slot);
		if (index > -1) {
			user_res.splice(index, 1);
		}
		res_failure += slot + '\n';
	}
	let cancel_failure = 'Cancellation failure:\n';
	for (let slot of response.cancel_failed) {
		document.getElementById(slot).classList.replace('dereserving', 'reserved');
		let index = user_cancel.indexOf(slot);
		if (index > -1) {
			user_res.splice(index, 1);
		}
		cancel_failure += slot + '\n';
	}
	let failure_alert = '';
	if (response.res_failed.length > 0) {
		failure_alert += res_failure;
	}
	if (response.cancel_failed.length > 0) {
		failure_alert += cancel_failure;
	}
	if (failure_alert != '') {
		alert(failure_alert + 'Reload page to see current state.');
	}
	else {
		alert('All reservations/cancellations succeeded.')
	}
}

function submit_changes() {
	let inputs = validate_inputs();
	if (inputs != null) {
		let xhr = new XMLHttpRequest;
		xhr.open('POST', '/reserve');
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.onload = function() {
			if (xhr.status == 200) {submission_results(JSON.parse(xhr.responseText));}
			else {alert('There was a problem with the server.')}
		};
		xhr.send(JSON.stringify(inputs));
	}
}

function cancel_dereserving(id, classes) {
	let index = user_cancel.indexOf(id);
	if (index > -1) {
		user_res.splice(index, 1);
	}
	classes.replace('dereserving', 'reserved');
}

function cancel_reserved(id, classes) {
	user_cancel.push(id);
	classes.replace('reserved', 'dereserving');
}

function cancel_reserving(id, classes) {
	let index = user_res.indexOf(id);
	if (index > -1) {
		user_res.splice(index, 1);
	}
	classes.replace('reserving', 'free');
}

function reserve_slot(id, classes) {
	if (user_res.length < 6) {
		user_res.push(id);
		classes.replace('free', 'reserving');
	}
	else {
		alert('You can reserve a maximum of 6 slots.')
	}
}

function slot_onclick(id) {
	let classes = document.getElementById(id).classList;
	if (classes.contains('free')) {
		reserve_slot(id, classes);
	}
	else if (classes.contains('reserving')) {
		cancel_reserving(id, classes);
	}
	else if (classes.contains('reserved')) {
		cancel_reserved(id, classes);
	}
	else if (classes.contains('dereserving')) {
		cancel_dereserving(id, classes);
	}
}
