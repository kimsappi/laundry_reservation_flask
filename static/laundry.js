function submit_changes() {
	
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
		alert('You can only reserve 6 slots.')
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
