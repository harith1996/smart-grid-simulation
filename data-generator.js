const deviceTypes = [
	{ type: "EV (Home charger) ", powerPivot: 7200, capacityPivot: 80000 },
	{ type: "EV (Public supercharger)", powerPivot: 9000, capacityPivot: 80000 },
	{ type: "Electric Bus", powerPivot: 10000, capacityPivot: 80000 },
	{ type: "Smartphone", powerPivot: 17, capacityPivot: 15.2 },
	{ type: "Laptop", powerPivot: 100, capacityPivot: 70 },
	{ type: "Bluetooth Speaker", powerPivot: 20, capacityPivot: 15 },
	{ type: "Home inverter", powerPivot: 1600, capacityPivot: 15000 }
];
let devices = [...Array(50).keys()].map((index) => {
    let deviceType = deviceTypes[Math.floor( Math.random() * deviceTypes.length)];
    let powerPivot = deviceType['powerPivot'];
    let capacityPivot = deviceType['capacityPivot'];
	return {
		id: deviceType['type'] + index,
		type: deviceType['type'],
        powerRating: getValueAroundPivot(powerPivot),
        capacity: getValueAroundPivot(capacityPivot)
	};
});

function getValueAroundPivot(pivot) {
    return (pivot + (Math.random() - 0.5) * pivot * 0.1).toFixed(0);
}
console.log(devices);
console.log(JSON.stringify(devices));

function (element) {
	return {
		"name" : element.innerHTML,
		"ogoal" : "cost",
		"ndevices" : Math.ceil(Math.random() * 7)
	  }
}