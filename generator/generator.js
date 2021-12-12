#!/usr/bin/env node
const fs = require('fs')
const cli = require('cli')
const { uniqueNamesGenerator, names } = require('unique-names-generator')

const options = cli.parse({
    devices: [ 'd', 'Number of devices to generate', 'int', 50],
    users: [ 'u', 'Number of users to generate', 'int', 50],
    file: [ 'f', 'File to write the data to', 'string', 'data.json'],
});

const deviceTypes = [
	{ type: "EV (Home charger)", powerPivot: 7200, canGenerate: true },
	{ type: "EV (Public supercharger)", powerPivot: 9000, canGenerate: false },
	{ type: "Electric Bus", powerPivot: 10000, canGenerate: true },
	{ type: "Smartphone", powerPivot: 17, canGenerate: false },
	{ type: "Laptop", powerPivot: 100, canGenerate: false },
	{ type: "Bluetooth Speaker", powerPivot: 20, canGenerate: false },
	{ type: "Home inverter", powerPivot: 1600, canGenerate: true }
];

const optGoals = ["cost"]

const nameGeneratorConfig = {
	dictionaries: [names, names],
	separator: ' ',
	length: 2
}

function randInt(min, max) { return Math.floor(Math.random() * (max - min) + min) }
function getValueAroundPivot(pivot) { return parseInt((pivot+(Math.random()-0.5)*pivot*0.1).toFixed(0)) }

let devices = [...Array(options.devices).keys()].map((index) => {
    let deviceType = deviceTypes[randInt(0, deviceTypes.length)];
    let powerPivot = deviceType['powerPivot'];
	return {
		id: index,
		name: `${deviceType['type']} ${index}`,
		type: deviceType['type'],
        power_limit: getValueAroundPivot(powerPivot),
		charge_profile: ((Math.random()) * 0.1),
		generator: (deviceType['canGenerate'] && (Math.random() - 0.5) > 0),
		curr_charge: Math.random()
	};
});

let users = [...Array(options.users).keys()].map((index) => {
	
	var devIndexes = new Set()
	var devSchedules = []

	var maxDevices = randInt(1, 8)
	for (let x = 0; x < maxDevices; x++) {
		devIndexes.add(randInt(0, devices.length))
	}
	
	var dayStart, dayEnd, hourStart, hourEnd
	for (let x = 0; x < devIndexes.size; x++) {
		dayStart = randInt(0, 6),
		dayEnd = randInt(dayStart+1, 7),
		hourStart = randInt(0, 23),
		hourEnd = randInt(hourStart+1, 24)
		hourStart = hourStart.toFixed(1)
		hourEnd = hourEnd.toFixed(1)
		devSchedules.push(
			`${dayStart}-${dayEnd}/${hourStart}-${hourEnd}`
		)
	}
	
	var user = {
		name: uniqueNamesGenerator(nameGeneratorConfig),
		ogoal: optGoals[randInt(0, optGoals.length)],
		devices: [...devIndexes],
        schedules: devSchedules
	};
	
	switch (user.ogoal) {
		case "cost":
			user['preferences']	= [randInt(15, 20).toFixed(1) / 10e5]
			break
		// Here we add options
		// for each target 
	}
	
	return user
});

fs.writeFileSync(options.file, JSON.stringify({seed: randInt(0, Number.MAX_SAFE_INTEGER), devices: devices, users: users}, null, '\t'));