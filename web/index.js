const SIM_UPDATE_INTERVAL = 500;
let userid;
let network;
let nodes, edges;

var socket = io();

let dataToSend = undefined

let updateInterval;

let container = document.getElementById("vis");
let fileInput = document.getElementById("file-input")
let fileSelected = document.getElementById("file-selected")
var toolbarTime = document.getElementById("toolbar-time");
const visOptions = {
	nodes: {
		shape: "dot",
		size: 8,
	},
	edges: {
		color: "#D3D3D3",
		width: 2,
	},
	physics: {
		forceAtlas2Based: {
			gravitationalConstant: -26,
			centralGravity: 0.005,
			springLength: 230,
			springConstant: 0.18,
		},
		maxVelocity: 146,
		solver: "forceAtlas2Based",
		timestep: 0.35,
		stabilization: { iterations: 150 },
	},
	interaction: {
		tooltipDelay: 50,
	},
};

function changeDataToSend(e) {
	var file = e.target.files[0];
	if (!file) { return }
	var reader = new FileReader();
	reader.onload = function (e) {
		fileSelected.innerText = `Loaded with "${file.name}"`
		dataToSend = e.target.result
	};
	reader.readAsText(file);
}

function uuidv4() {
	return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
		(
			c ^
			(crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
		).toString(16)
	);
}

function initSim() {
	var opts = document.getElementById("options");
	opts.classList.add(
		"animate__animated",
		"animate__fadeOut",
		"animate__faster"
	);
	opts.addEventListener("animationend", () => {
		var hiddenElements = document.querySelectorAll(".hidden-until-init");
		hiddenElements.forEach((e) => {
			e.classList.remove("hidden-until-init");
			e.classList.add("animate__animated");
		});
	});
	userid = uuidv4();
	console.log(dataToSend)
	socket.emit("init", { userid: userid, data: dataToSend });
}

socket.on("init-res", function (data) {
	preprocess(data);
	nodes = new vis.DataSet(data.nodes);
	edges = new vis.DataSet(data.edges);
	toolbarTime.innerText = new Date().toLocaleTimeString();
	network = new vis.Network(
		container,
		{ nodes: nodes, edges: edges },
		visOptions
	);
	socket.emit("get-grid-info", { userid: userid });
});

function updateSim() {
	if (updateInterval == undefined) {
		updateInterval = setInterval(() => {
			toolbarTime.innerText = new Date().toLocaleTimeString();
			socket.emit("update", { userid: userid });
		}, SIM_UPDATE_INTERVAL);
	}
}

function updateDashboard(type, data) {
	const statElements = document.querySelectorAll(
		`#grid-${type} .dashboard-stat-value span`
	);
	statElements.forEach((element) => {
		const id = element.id;
		element.innerHTML = data[id] || "";
	});
	console.log(data);
}

socket.on("get-grid-info-res", updateDashboard.bind(this, "info"));

socket.on("get-grid-status-res", updateDashboard.bind(this, "status"));

socket.on("update-res", function (data) {
	preprocess(data);
	nodes.update(data.nodes);
	edges.update(data.edges);
	edges.remove(data.unlinks);
});

function preprocess(data) {
	data.nodes.forEach(node => {
		if (node.title)
			node.title = formatTitle(node.title);
	})
}


function formatTitle(titleString) {
	const tooltip = document.createElement('div');
	tooltip.innerHTML = '';
	tooltip.innerHTML = "<div class='node-tooltip'><table><tr><th>Property</th><th>Value</th></tr></table></div>";
	const tooltipTable = tooltip.querySelector('table');
	const titleData = JSON.parse(titleString);
	Object.keys(titleData).forEach(property => {
		if (['string', 'number', 'boolean'].includes(typeof titleData[property])) {
			const tr = document.createElement('tr');
			const propTd = document.createElement('td');
			const valTd = document.createElement('td');
			propTd.innerHTML = property;
			valTd.innerHTML = titleData[property];
			tr.appendChild(propTd);
			tr.appendChild(valTd);
			tooltipTable.appendChild(tr);
		}
	});
	return tooltip;
}

function skipSim() {
	clearInterval(updateInterval);
	updateInterval = undefined;
	socket.emit("skip", { userid: userid });
}

socket.on("skip-res", function (data) {
	nodes.update(data.nodes);
	edges.update(data.edges);
	edges.remove(data.unlinks);
});

function pauseSim() {
	clearInterval(updateInterval);
	updateInterval = undefined;
}

fileInput.addEventListener('change', changeDataToSend, false);