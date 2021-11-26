const deviceTypes = [
	{ type: "EV (Home charger) ", powerPivot: 7200, capacityPivot: 80000, canGenerate: true },
	{ type: "EV (Public supercharger)", powerPivot: 9000, capacityPivot: 80000, canGenerate: false },
	{ type: "Electric Bus", powerPivot: 10000, capacityPivot: 80000, canGenerate: true },
	{ type: "Smartphone", powerPivot: 17, capacityPivot: 15.2, canGenerate: false },
	{ type: "Laptop", powerPivot: 100, capacityPivot: 70, canGenerate: false },
	{ type: "Bluetooth Speaker", powerPivot: 20, capacityPivot: 15, canGenerate: false },
	{ type: "Home inverter", powerPivot: 1600, capacityPivot: 15000, canGenerate: true }
];
let devices = [...Array(50).keys()].map((index) => {
    let deviceType = deviceTypes[Math.floor( Math.random() * deviceTypes.length)];
    let powerPivot = deviceType['powerPivot'];
    let capacityPivot = deviceType['capacityPivot'];
	return {
		id: index,
		name: deviceType['type'] + index,
		type: deviceType['type'],
        power_limit: getValueAroundPivot(powerPivot),
        capacity: getValueAroundPivot(capacityPivot),
		load_profile: ((Math.random()) * 0.1),
		generator: (deviceType['canGenerate'] && (Math.random() - 0.5) > 0) ? true : false,
		curr_charge: (Math.random())/4
	};
});

function getValueAroundPivot(pivot) {
    return (pivot + (Math.random() - 0.5) * pivot * 0.1).toFixed(0);
}
console.log(devices);
console.log(JSON.stringify(devices));